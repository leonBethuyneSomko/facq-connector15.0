# -*- coding: utf-8 -*-
import json
import logging
import os
import subprocess
import tempfile

import odoo
import odoo.release
import odoo.sql_db
import odoo.tools
from odoo import SUPERUSER_ID
from odoo.tools import find_pg_tool, exec_pg_environ

_logger = logging.getLogger(__name__)

from odoo.service import db
from odoo.service.db import check_db_management_enabled, dump_db_manifest

restore_db_old = db.restore_db


def _archive_cron_jobs(db_name):
    try:
        _logger.info('Archiving cron jobs.')
        db = odoo.sql_db.db_connect(db_name)
        with db.cursor() as cr:
            # cr.autocommit(True)
            cr._cnx.autocommit = True
            query = """
                UPDATE ir_cron
                SET to_restore = TRUE,
                    active = FALSE
                WHERE active = TRUE
            """

            cr.execute(query)
            cr.commit()
    except Exception:
        _logger.info('Archiving crons jobs failed.')


@check_db_management_enabled
def restore_db_new(db, dump_file, copy=False):
    restore_db_old(db, dump_file, copy=copy)

    registry = odoo.modules.registry.Registry.new(db)
    with registry.cursor() as cr:
        env = odoo.api.Environment(cr, SUPERUSER_ID, {})
        if os.environ.get('SOMKOENV', 'PROD').lower() != 'prod':
            _archive_cron_jobs(db)
            env['ir.mail_server'].search([('active', '=', True)]).write({'active': False})
            env['fetchmail.server'].search([('active', '=', True)]).write({'active': False})
            _logger.info('Archived cron jobs, incoming and outgoing mail servers : %s', db)
            for icon in env['ir.ui.menu'].with_context({'ir.ui.menu.full_list': True}).search([('web_icon', '!=', False)]):
                icon.write({'web_icon': icon.web_icon})
            if os.environ.get('SOMKOENV', 'PROD').lower() == 'dev':
                env['res.users'].browse(2).write({'password': 'admin'})
                _logger.info('Admin password (user 2) was reset to \'admin\': %s', db)

db.restore_db = restore_db_new

dump_db_old = db.dump_db


@check_db_management_enabled
def dump_db_new(db_name, stream, backup_format='zip'):
    """Dump database `db` into file-like object `stream` if stream is None
    return a file object with the dump """
    if backup_format == 'empty_zip':
        _logger.info('DUMP DB: %s format %s', db_name, backup_format)

        cmd = [find_pg_tool('pg_dump'), '--no-owner', db_name]
        env = exec_pg_environ()
        with tempfile.TemporaryDirectory() as dump_dir:
            os.mkdir(os.path.join(dump_dir, 'filestore'))
            with open(os.path.join(dump_dir, 'filestore', 'temp.txt'), 'w') as file:
                pass
            with open(os.path.join(dump_dir, 'manifest.json'), 'w') as fh:
                db = odoo.sql_db.db_connect(db_name)
                with db.cursor() as cr:
                    json.dump(dump_db_manifest(cr), fh, indent=4)
            cmd.insert(-1, '--file=' + os.path.join(dump_dir, 'dump.sql'))
            subprocess.run(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=True)
            if stream:
                odoo.tools.osutil.zip_dir(dump_dir, stream, include_dir=False,
                                          fnct_sort=lambda file_name: file_name != 'dump.sql')
            else:
                t = tempfile.TemporaryFile()
                odoo.tools.osutil.zip_dir(dump_dir, t, include_dir=False,
                                          fnct_sort=lambda file_name: file_name != 'dump.sql')
                t.seek(0)
                return t
    else:
        return dump_db_old(db_name, stream, backup_format=backup_format)

db.dump_db = dump_db_new

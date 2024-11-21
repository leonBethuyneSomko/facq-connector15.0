# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import datetime
import logging

import odoo
import odoo.modules.registry
import werkzeug
import werkzeug.exceptions
import werkzeug.utils
import werkzeug.wrappers
import werkzeug.wsgi
from lxml import html
from odoo import http
from odoo.addons.base.models.ir_qweb import render as qweb_render
from odoo.addons.web.controllers.database import Database, DBNAME_PATTERN
from odoo.exceptions import AccessError
from odoo.http import content_disposition, dispatch_rpc, request
from odoo.tools.misc import file_open

_logger = logging.getLogger(__name__)


class DatabaseController(Database):

    @http.route('/web/database/backup', type='http', auth="none", methods=['POST'], csrf=False)
    def backup(self, master_pwd, name, backup_format='zip'):
        if backup_format == 'empty_zip':
            insecure = odoo.tools.config.verify_admin_password('admin')
            if insecure and master_pwd:
                dispatch_rpc('db', 'change_admin_password', ["admin", master_pwd])
            try:
                odoo.service.db.check_super(master_pwd)
                ts = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f'{name}_{ts}.zip'
                headers = [
                    ('Content-Type', 'application/octet-stream; charset=binary'),
                    ('Content-Disposition', content_disposition(filename)),
                ]
                dump_stream = odoo.service.db.dump_db(name, None, backup_format)
                response = werkzeug.wrappers.Response(dump_stream, headers=headers, direct_passthrough=True)
                return response
            except Exception as e:
                _logger.exception('Database.backup')
                error = "Database backup error: %s" % (str(e) or repr(e))
                return self._render_template(error=error)
        else:
            return super().backup(master_pwd, name, backup_format=backup_format)

    def _render_template(self, **d):
        d.setdefault('manage', True)
        d['insecure'] = odoo.tools.config.verify_admin_password('admin')
        d['list_db'] = odoo.tools.config['list_db']
        d['langs'] = odoo.service.db.exp_list_lang()
        d['countries'] = odoo.service.db.exp_list_countries()
        d['pattern'] = DBNAME_PATTERN
        # databases list
        try:
            d['databases'] = http.db_list()
            d['incompatible_databases'] = odoo.service.db.list_db_incompatible(d['databases'])
        except odoo.exceptions.AccessDenied:
            d['databases'] = [request.db] if request.db else []

        templates = {}

        with file_open("environment/static/src/public/new_database_manager.qweb.html", "r") as fd:
            templates['database_manager'] = fd.read()
        with file_open("web/static/src/public/database_manager.master_input.qweb.html", "r") as fd:
            templates['master_input'] = fd.read()
        with file_open("web/static/src/public/database_manager.create_form.qweb.html", "r") as fd:
            templates['create_form'] = fd.read()

        def load(template_name):
            fromstring = html.document_fromstring if template_name == 'database_manager' else html.fragment_fromstring
            return fromstring(templates[template_name]), template_name

        return qweb_render('database_manager', d, load)

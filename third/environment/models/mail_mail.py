from odoo import models, api
from odoo.exceptions import UserError

from .ir_config_parameter import get_env


class FetchmailServer(models.Model):
    _inherit = 'fetchmail.server'

    @api.model
    def _fetch_mails(self, *args, **kwargs):
        if not bool(int(self.env['ir.config_parameter'].get_param(get_env() + '.mail'))):
            raise UserError('This server does not consume emails, because it is in test mode!')
        return super(FetchmailServer, self)._fetch_mails(*args, **kwargs)

    def fetch_mail(self):
        if not bool(int(self.env['ir.config_parameter'].get_param(get_env() + '.mail'))):
            raise UserError('This server does not consume emails, because it is in test mode!')
        return super(FetchmailServer, self).fetch_mail()

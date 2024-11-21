from odoo import models
from odoo.exceptions import UserError

from .ir_config_parameter import get_env


class FetchmailServer(models.Model):
    """Incoming POP/IMAP mail server account"""

    _inherit = 'fetchmail.server'

    def connect(self, *args, **kwargs):
        if not bool(int(self.env['ir.config_parameter'].get_param(get_env() + '.mail'))):
            raise UserError('This server does not consume emails, because it is in test mode!')
        return super(FetchmailServer, self).connect(*args, **kwargs)

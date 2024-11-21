from odoo import models

from .ir_config_parameter import get_env


class IrMailServer(models.Model):
    _inherit = 'ir.mail_server'

    def connect(self, *args, **kwargs):
        if not bool(int(self.env['ir.config_parameter'].sudo().get_param(get_env() + '.mail'))):
            raise Exception('This server does not send mails, because it is in test mode!')

        return super(IrMailServer, self).connect(*args, **kwargs)

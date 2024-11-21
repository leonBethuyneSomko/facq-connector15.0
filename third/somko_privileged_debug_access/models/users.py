from odoo import models, api, fields


class Users(models.Model):
    _inherit = 'res.users'

    is_debug_mode_enabled = fields.Boolean(string='Debug Mode Enabled')

    @api.model
    def _init_debug_mode_enabled(self):
        self.browse([1, 2]).write({
            'is_debug_mode_enabled': True
        })

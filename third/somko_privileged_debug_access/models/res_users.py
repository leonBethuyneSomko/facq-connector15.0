from odoo import models, api, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    debug_mode_enabled = fields.Boolean(string='Debug Mode Enabled', default=False)

    @api.model
    def _init_debug_mode_enabled(self):
        self.browse([1, 2]).write({'debug_mode_enabled': True})

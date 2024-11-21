import os

from odoo import models, api


def get_env():
    return os.environ.get('SOMKOENV', "PROD").lower()


def update_key(key):
    somko_env = get_env()
    if somko_env in ['test', 'dev']:
        key = '.'.join([somko_env, key])
    return key


class IrConfigParameter(models.Model):
    _inherit = 'ir.config_parameter'

    @api.model
    def get_param(self, key, default=False):
        new_key = super(IrConfigParameter, self).get_param(update_key(key))
        if not new_key:
            return super(IrConfigParameter, self).get_param(key, default)
        return new_key

    @api.model
    def set_param(self, key, value):
        new_key = super(IrConfigParameter, self).get_param(update_key(key))
        if not new_key:
            return super(IrConfigParameter, self).set_param(key, value)
        return super(IrConfigParameter, self).set_param(update_key(key), value)

    @api.model
    def init_param(self, key, value):
        if not self.get_param(update_key(key)):
            self.set_param(key, value)

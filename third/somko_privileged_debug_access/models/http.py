from odoo import models
from odoo.http import request
from odoo.tools.misc import str2bool


class Http(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _handle_debug(cls):
        # Store URL debug mode (might be empty) into session
        if 'debug' in request.httprequest.args:
            debug_mode = []
            for debug in request.httprequest.args['debug'].split(','):
                if debug not in ['', '1', 'assets', 'tests']:
                    debug = '1' if str2bool(debug, debug) else ''

                debug_mode.append(debug)

            debug_mode = ','.join(debug_mode)

            # Write on session only when needed
            if debug_mode != request.session.debug and request.env['res.users'].browse(request.session.uid).is_debug_mode_enabled:
                request.session.debug = debug_mode

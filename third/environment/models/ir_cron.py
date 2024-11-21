import logging

from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)
from .ir_config_parameter import get_env


class IrCron(models.Model):
    _inherit = 'ir.cron'

    to_restore = fields.Boolean(string="To Restore", default=False)
    required = fields.Boolean(string="Required", default=False)

    email_template_id = fields.Many2one(
        comodel_name="mail.template",
        string="Error E-mail Template",
        help="Select the email template that will be sent when "
             "this scheduler fails."
    )

    @api.model
    def _handle_callback_exception(self, cron_name, server_action_id, job_id, job_exception):
        res = super(IrCron, self)._handle_callback_exception(cron_name,
                                                             server_action_id,
                                                             job_id,
                                                             job_exception)
        my_cron = self.browse(job_id)

        if my_cron.email_template_id:
            # we put the job_exception in context to be able to print it inside
            # the email template
            context = {
                'job_exception': job_exception,
                'dbname': self._cr.dbname,
            }

            _logger.info(
                "Sending scheduler error email with context=%s", context)

            self.env['mail.template'].browse(
                my_cron.email_template_id.id
            ).with_context(context).sudo().send_mail(
                my_cron.id, force_send=True)

        return res

    @api.model
    def _test_scheduler_failure(self):
        """This function is used to test and debug this module."""
        raise UserError(
            _("Task failure with UID = %d.") % self._uid)

    @api.model
    def validate(self):
        _logger.info("Checking for inactive required jobs")
        job_ids = self.with_context(active_test=False).search([('required', '=', True), ('active', '=', False)])

        if len(job_ids) > 0:
            _logger.error("Not all required cronjobs are activated.")
            validate_job = self.env.ref('environment.ir_cron_validation')
            if validate_job.email_template_id:
                # we put the job_exception in context to be able to print it inside
                # the email template
                context = {
                    'dbname': self._cr.dbname,
                }

                _logger.info(
                    "Sending scheduler error email with context=%s", context)

                self.env['mail.template'].browse(
                    validate_job.email_template_id.id
                ).with_context(context).sudo().send_mail(
                    validate_job.id, force_send=True)

    def write(self, values):
        if 'active' in values:
            validate_job = self.env.ref('environment.ir_cron_validation')
            jobs = self - validate_job
            if len(jobs) > 0:
                values['to_restore'] = not values['active']
                return super(IrCron, jobs).write(values)
            else:
                return True

        return super(IrCron, self).write(values)

    def unlink(self):
        for record in self:
            validate_job = self.env.ref('environment.ir_cron_validation')
            if record == validate_job:
                continue
            super(IrCron, record).unlink()

        return True

    @classmethod
    def _process_job(cls, db, cron_cr, job):
        env = api.Environment(cron_cr, SUPERUSER_ID, {})
        if not bool(int(env['ir.config_parameter'].get_param(get_env() + '.cron'))):
            _logger.info('Skipping cron jobs. This server runs in test mode')
        else:
            super()._process_job(db, cron_cr, job)

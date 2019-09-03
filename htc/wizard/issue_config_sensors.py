from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date


class IssueConfigSensor(models.TransientModel):
    _name = "htc.issue_config_sensor_wizard"
    issue_template_code = fields.Char('Template Code')

    @api.model
    def default_site(self):
        id = self.env.context.get('site_id')
        site = self.env['htc.site'].browse(int(id))
        return site.id

    site_id = fields.Many2one(
        "htc.site", "Site", default=default_site, required=True)

    sensor_ids = fields.Many2many("htc.sensor", string="Sensors")

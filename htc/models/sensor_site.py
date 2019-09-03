# -*- coding: utf-8 -*-
from odoo import api, fields, models
import datetime


class SensorSite(models.Model):
    _name = 'htc.sensor.sites'
    _inherit = 'mail.thread'

    name = fields.Char("Sensor-Site", compute="get_name", readonly=True)
    sensor_id = fields.Many2one(
        "htc.sensor", "Sensor Mac Address", required=True)
    site_id = fields.Many2one("htc.site", "Site Name", required=True)
    file_name_field_template_id = fields.Many2one(
        "htc.file_name_field_template", "Template Code", required=True)
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    status = fields.Boolean("Active / Inactive", default=True)

    site_group_id = fields.Integer(
        string=u'Site Group', compute="_get_site_group_id", store=False)

    def get_name(self):
        if self.sensor_id and self.site_id:
            self.name = str(self.sensor_id.mac_address) + ' - ' + str(
                self.site_id.site_name)

    @api.multi
    @api.depends('site_id')
    def _get_site_group_id(self):
        for rec in self:
            self.site_group_id = rec.site_id.site_group_id

    def toggle_status(self):
        if self.status is True:
            record = super(SensorSite, self).write({
                'status': not self.status,
                'end_date': datetime.datetime.now().date()
            })
            return record
        else:
            record = super(SensorSite, self).write({
                'status': not self.status,
                'end_date': None
            })
            return record

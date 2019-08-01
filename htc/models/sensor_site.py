# -*- coding: utf-8 -*-
from odoo import api, fields, models

class SensorSite(models.Model):
    _name = 'htc.sensor.sites'
    _inherit = 'mail.thread'

    sensor_id = fields.Many2one("htc.sensor","Sensor Mac Address", required=True)
    site_id = fields.Many2one("htc.site", "Site Code", required=True)
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    status = fields.Boolean("Active / Inactive", default=True)
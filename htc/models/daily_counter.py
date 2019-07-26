# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class DailyCounter(models.Model):
    _name = 'htc.daily_counter'
    site_id = fields.Many2one("htc.site", string="Site", required=True)
    sensor_id = fields.Many2one("htc.sensor", string="Sensor", required=True)
    transaction_date = fields.Date("Transaction Date", required=True)
    daily_total_in = fields.Integer("Daily Total In", required=True, default=0)
    daily_total_out = fields.Integer("Daily Total Out", required=True, default=0)
    alert_count = fields.Integer("Alert Count", required=True, default=0)

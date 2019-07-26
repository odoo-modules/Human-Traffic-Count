# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class SensorTransaction(models.Model):
    _name = 'htc.sensor_transaction'
    site_id = fields.Many2one("htc.site", string="Site", required=True)
    sensor_id = fields.Many2one("htc.sensor", string="Sensor", required=True)
    transaction_date = fields.Datetime("Transaction Date", required=True)
    in_count = fields.Integer("Total In", required=True)
    out_count = fields.Integer("Total Out", required=True)
    status = fields.Boolean("Status", default=True)
    process_count = fields.Integer("Process Count", default=0)
    week = fields.Integer("Week", required=True)
    day = fields.Integer("Day", required=True)
    method = fields.Char("Method")












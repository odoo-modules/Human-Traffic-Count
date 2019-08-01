# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models
import json as simplejson


class Site(models.Model):
    _name = 'htc.site'
    _inherit = 'mail.thread'

    site_group_id = fields.Many2one("htc.site.group",
                                    string="Site Group Code",
                                    requierd=True)
    site_name = fields.Char("Site Name", required=True)
    site_code = fields.Char("Site Code", required=True)
    delivery_method = fields.Selection([("ftp", "FTP"), ('email', 'Email'),
                                        ('real_time', 'Real Time'),
                                        ('batch', 'Batch')],
                                       string="Delivery Method",
                                       required=True)
    group_ids = fields.One2many("htc.group", "site_id", string="Groups")
    daily_counter_ids = fields.One2many("htc.daily_counter",
                                        "site_id",
                                        string="Daily Counts")
    _sql_constraints = [
        ('prefix_code_unique', 'UNIQUE(site_code)',
         "Can't be duplicate value for Prefix and Site Group Code!")
    ]
    server_address = fields.Char("Server Address", requierd=True)
    user_id = fields.Char("User Name", requierd=True)
    password = fields.Char("Password", requierd=True)
    http_port = fields.Char("Http Port")
    https_port = fields.Char("Https Port")
    timezone_name = fields.Char("Timezone Name")
    ip_range = fields.Char("IP Range", requierd=True)
    interface_code = fields.Char("Interface Code")

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            code = record.site_code
            result.append((record.id, code))
        return result

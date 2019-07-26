# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class SiteGroup(models.Model):
    _name = 'htc.sitegroup'
    _inherit = 'mail.thread'

    name = fields.Char("Site Group Name", required=True)
    code = fields.Char("Site Group Code", required=True)
    sensor_ids = fields.One2many("htc.sensor", "sitegroup_id", string="Sensors")
    site_ids = fields.One2many("htc.site", "site_group_id", string="Sites")
    _sql_constraints = [
        ('code_unique', 'unique(code)', "Can't be duplicate value for Site Group Code!")
    ]

    @api.onchange('code')
    def do_stuff(self):
        if self.code:
            self.code = str(self.code).upper()
        else:
            self.code = ""

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            code = record.code
            result.append((record.id, code))
        return result



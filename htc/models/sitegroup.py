# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class SiteGroup(models.Model):
    _name = 'htc.site.group'
    _inherit = 'mail.thread'

    site_group_name = fields.Char("Site Group Name", required=True)
    site_group_code = fields.Char("Site Group Code", required=True)
    license_code = fields.Char("Site Group License Code", required=True)
    sensor_ids = fields.One2many("htc.sensor","site_group_id","Sensors")
    _sql_constraints = [
        ('site_group_code_unique', 'unique(site_group_code)', "Can't be duplicate value for Site Group Code!")
    ]

    @api.onchange('site_group_code')
    def do_stuff(self):
        if self.site_group_code:
            self.site_group_code = str(self.site_group_code).upper()
        else:
            self.site_group_code = ""

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            code = record.site_group_code
            result.append((record.id, code))
        return result



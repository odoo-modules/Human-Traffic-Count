# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class Group(models.Model):
    _name = 'htc.group'
    _inherit = 'mail.thread'
    name = fields.Char("Group Name", required=True)
    code = fields.Char("Group Code", required=True)
    site_id = fields.Many2one("htc.site", string="Site", requierd=True)
    group_sensor_ids = fields.One2many('htc.group_sensors',
                                       "group_id",
                                       string="Group Sensors")
    _sql_constraints = [('code_unique', 'unique(site_id,code)',
                         "Can't be duplicate value for Site and Group Code!")]

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

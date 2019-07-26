# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models
import json as simplejson


class Site(models.Model):
    _name = 'htc.site'
    _inherit = 'mail.thread'
    name = fields.Char("Site Name", required=True)
    code = fields.Char("Site Code", required=True)
    site_group_id = fields.Many2one("htc.sitegroup", string="Site Group Code", requierd=True)
    group_ids = fields.One2many("htc.group", "site_id", string="Groups")
    daily_counter_ids = fields.One2many("htc.daily_counter","site_id", string="Daily Counts")
    _sql_constraints = [
        ('prefix_code_unique', 'unique(code)', "Can't be duplicate value for Prefix and Site Group Code!")
    ]
    prefix = fields.Char(compute='_get_prefix', store=True, string="Prefix")
    ip_range=fields.Char("IP Range")
    interface_code = fields.Char("Interface Code")
    credential_id = fields.Char("User Id", requierd=True)
    password = fields.Char("Password", requierd=True)
    ftp_server_url = fields.Char("FTP Server Address", requierd=True)
    sersor_ids = fields.One2many("htc.sensor", "site_id", string="Sensors")

    def write (self, values):
        values['prefix'] = self.prefix
        return super(Site, self).write(values)

    @api.depends('site_group_id')
    def _get_prefix (self):
        for site in self:
            if site.site_group_id:
                site.prefix = ""
                sg_code = site.site_group_id.code
                site.prefix = sg_code
            else:
                site.prefix = ""

    @api.onchange('code')
    def _get_prefix_zero (self):
        for site in self:
            if site.code:
                code_prefix = ''
                code_len = len(site.code)
                for x in range(5 - code_len):
                    code_prefix = code_prefix + '0'
                site.code = code_prefix + site.code
            else:
                site.prefix = ""

    @api.multi
    def name_get (self):
        result = []
        for record in self:
            code = record.prefix + '-' + record.code
            result.append((record.id, code))
        return result

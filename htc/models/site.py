# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models
import json as simplejson
import datetime


class FileFormat(models.Model):
    _name = 'file.format'

    name = fields.Char("Name")
    value = fields.Char("Value")

    @api.model
    def init(self):
        switcher = {
            "#S": "Site Name",
            "#I": "Site Id",
            "#D": "Date",
            "#T": "Time",
            "#M": "Mac Address"
        }
        search_value = ["#S", "#I", "#D", "#T", "#M"]
        values = []
        for val in search_value:
            result = self.search([("name", "=", val)])
            if not result:
                values.append({'name': val})
            else:
                result[0].value = switcher.get(result[0].name)
                self.write(result)
        if len(values) > 0:
            result = self.create(values)

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            value = record.value
            result.append((record.id, value))
        return result


class Site(models.Model):
    _name = 'htc.site'
    _inherit = 'mail.thread'

    site_group_id = fields.Many2one(
        "htc.site.group", string="Site Group Code", requierd=True)
    site_name = fields.Char("Site Name", required=True)
    site_code = fields.Char("Site Code", required=True)
    delivery_method = fields.Selection([("ftp", "FTP"), ('email', 'Email'),
                                        ('real_time', 'Real Time'),
                                        ('batch', 'Batch')],
                                       string="Delivery Method",
                                       required=True)
    group_ids = fields.One2many("htc.group", "site_id", string="Groups")
    daily_counter_ids = fields.One2many(
        "htc.daily_counter", "site_id", string="Daily Counts")
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
    interface_code = fields.Char("Interface Code", required=True)
    debug_mode_enable = fields.Boolean("Debug Mode Enable", default=False)
    # file_name = fields.Selection([("Site name", "#S"), ("Site Id", "#I"),
    #                               ("Date", "#D"), ("Time", "#T"),
    #                               ("Mac address", "#M")],
    #                              string="Import File Name Format")
    file_name = fields.Many2many(
        "file.format", string="File Name Format", required=True)
    site_file_name_format = fields.Char(
        compute="get_file_name", store=False, string="Example File Name")

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            code = record.site_code
            result.append((record.id, code))
        return result

    @api.multi
    @api.depends('file_name')
    def get_file_name(self):
        switcher = {
            "#S": "site_name",
            "#I": "site_code",
            "#D": str(datetime.datetime.today().strftime('%y%m%d')),
            "#T": "000000",
            "#M": "xx:xx:xx:xx:xx:xx"
        }
        result_name = ""
        for fnames in self.mapped('file_name'):
            for fname in fnames:
                result = ""
                if fname.name == "#S" or fname.name == "#I":
                    result = self[switcher.get(fname.name)]
                else:
                    result = switcher.get(fname.name)
                if len(result_name) > 0:
                    result_name += "." + result
                else:
                    result_name += result
        if len(result_name) > 0:
            self.site_file_name_format = result_name + ".xml"

# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Sensor(models.Model):
    _name = 'htc.sensor'
    _inherit = 'mail.thread'
    key = 'z@nd0Techn010Gy'

    site_group_id = fields.Many2one("htc.site.group", "Site Group", required=True)
    mac_address = fields.Char("Mac Address", required=True)
    xml_format = fields.Selection([
        ('Xml 1', 'Xml 1'),
        ('Xml 2', 'Xml 2'),
        ('Latest', 'Latest')
    ],string="XML Format", default='Latest', required=True)
    device_name = fields.Char("Device Name")
    division_id = fields.Char("Division Id", default="")
    sensor_id = fields.Char("Sensor Id", default="")
    sensor_name = fields.Char("Sensor Name", default="")
    hardware_release_version = fields.Char("Hardware Release Version", default="")
    serial_number = fields.Char("Serial Number", default="")
    software_release = fields.Char("Software Version", default="")
    host_name  = fields.Char("Host Name", default="")
    ip_address = fields.Char("IP Address")
    sensor_site_ids = fields.One2many("htc.sensor.sites","sensor_id","Sensor_Site")
    site_code = fields.Char(compute="get_site",store=False,string="Site")
    status = fields.Boolean("Active/Inactive", compute="get_status")

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            mac_address = record.mac_address
            result.append((record.id, mac_address))
        return result

    @api.one
    @api.depends('sensor_site_ids')
    def get_site(self):
        for ssi in self.mapped('sensor_site_ids'):
            if ssi.status == True:
                for record in self:
                    record.site_code = ssi.site_id.site_code
    @api.one
    @api.depends('sensor_site_ids')
    def get_status(self):
        for ssi in self.mapped('sensor_site_ids'):
            if ssi.status == True:
                for record in self:
                    record.status = True
        # result = []
        # for record in self:
        #     if record.sensor_site_ids and record.sensor_site_ids[0].site_id:
        #         record.site_code=record.sensor_site_ids[0].site_id.site_code
        #     else:
        #         record.site_code=''       
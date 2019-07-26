# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad
# from base64 import b64encode, b64decode


class Sensor(models.Model):
    _name = 'htc.sensor'
    _inherit = 'mail.thread'
    key = 'z@nd0Techn010Gy'

    sensor_mac_address = fields.Char("Mac Address", required=True)
    license_code = fields.Char("License Code", required=True, default=" ")
    device_id = fields.Char("Device Id")
    device_name = fields.Char("Device Name")
    sitegroup_id = fields.Many2one("htc.sitegroup", "Site Group", required=True)
    site_id = fields.Many2one("htc.site", "Site")
    daily_counter_ids = fields.One2many("htc.daily_counter", "sensor_id", string="Daily Counts")
    xml_data_format = fields.Selection([
        ('Xml 1', 'Xml 1'),
        ('Xml 2', 'Xml 2'),
        ('Latest', 'Latest')
    ], default='Latest', required=True)
    group_sensor_ids = fields.One2many("htc.group_sensors", "sensor_id", string="Group Sensors")

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            mac_address = record.sensor_mac_address
            result.append((record.id, mac_address))
        return result

    # def encrypt_licnese(self):
    #     cipher = AES.new(b64decode(self.key), AES.MODE_CBC, iv=b'0123456789abcdef')
    #     padded_data = pad(self.license_code.encode(), cipher.block_size)
    #     cipher_text = cipher.encrypt(padded_data)
    #     print(b64encode(cipher_text))
    #
    # def decrypt_license(self):
    #     obj2 = AES.new(b64decode(self.key), AES.MODE_CBC, iv=b'0123456789abcdef')
    #     obj2.decrypt(self.license_code)

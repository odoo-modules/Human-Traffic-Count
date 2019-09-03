# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models
import json as simplejson
import datetime


class Site(models.Model):
    _name = 'htc.site'
    _inherit = 'mail.thread'
    site_group_id = fields.Many2one(
        "htc.site.group", string="Site Group Name", requierd=True)
    site_name = fields.Char("Site Name", required=True)
    site_code = fields.Char("Site Code", required=True, size=4)
    group_ids = fields.One2many("htc.group", "site_id", string="Groups")
    daily_counter_ids = fields.One2many(
        "htc.daily_counter", "site_id", string="Daily Counts")
    _sql_constraints = [
        ('prefix_code_unique', 'UNIQUE(site_code)',
         "Can't be duplicate value for Prefix and Site Group Code!")
    ]

    timezone_name = fields.Char("Timezone Name")
    ip_range = fields.Char("IP Range", requierd=True)
    interface_code = fields.Char("Interface Code")
    debug_mode_enable = fields.Boolean("Debug Mode Enable", default=False)
    file_name_field_template_ids = fields.Many2many(
        "htc.file_name_field_template",
        string="Site File Name Fields",
        required=True)

    sensor_site_ids = fields.One2many("htc.sensor.sites", "site_id",
                                      "Sensor_Site")

    ### FTP ###
    ftp_enable = fields.Boolean("Enable FTP")
    ftp_server_url = fields.Char("Server Address")
    ftp_server_port = fields.Char("Server Port")
    ftp_destination = fields.Char("Destination/ Url")
    ftp_aggretation_level = fields.Selection([
        ('5 miniutes', '5 miniutes'),
        ('15 miniutes', '15 miniutes'),
        ('30 miniutes', '30 miniutes'),
        ('60 miniutes', '60 miniutes'),
    ], "Aggretation Level")
    ftp_current_aggretation_level = fields.Char("Current Aggretation Level")
    ftp_delivery_format = fields.Selection(
        string=u'Delivery Fromat',
        selection=[('xml', 'xml'), ('pipe delimited', 'pipe delimited')])

    ftp_delivery_schdule = fields.Selection(
        string=u'Delivery Schedule',
        selection=[('15 miniutes', '15 miniutes'), ('Hourly', 'Hourly'),
                   ('Daily', 'Daily')])
    ftp_current_delivery_schdule = fields.Char("Current Delivery Schedule")
    ftp_max_attempts = fields.Integer("Max Attempts")
    ftp_retry_level = fields.Integer("Retry Level")
    # ftp_enable_authentication = fields.Boolean("Enable Authentication")
    ftp_user_name = fields.Char("User Name")
    ftp_password = fields.Char("Password")
    ftp_ftps = fields.Boolean("FTPS")
    ftp_sni_host_name = fields.Char("SNI Host Name")
    ftp_enable_external_ip = fields.Boolean("Enable External Ip")
    ftp_exteranl_ip = fields.Char("External Ip/ Override Ip")
    ftp_enable_port_range = fields.Boolean("Enable Port Range")
    ftp_lowest_port = fields.Integer("Lowest Port")
    ftp_highest_port = fields.Integer("Highest Port")

    ### Email ###
    email_enable = fields.Boolean("Enable Email")
    email_server_url = fields.Char("SMTP Server/ Host Name")
    email_server_port = fields.Char("Server Port")
    email_sender_email_address = fields.Char("Sender Email Address")
    email_recipient_email_address = fields.Char("Recipient Email Address")
    email_aggretation_level = fields.Selection([
        ('5 miniutes', '5 miniutes'),
        ('15 miniutes', '15 miniutes'),
        ('30 miniutes', '30 miniutes'),
        ('60 miniutes', '60 miniutes'),
    ], "Aggretation Level")
    email_delivery_time = fields.Char("Delivery Time")
    email_enable_authentication = fields.Boolean("Enable Authentication")
    email_user_name = fields.Char("User Name")
    email_password = fields.Char("Password")

    ### Batch 1###
    batch1_enable = fields.Boolean("Enable Batch 1")
    batch1_server_url = fields.Char("Server Address")
    batch1_server_port = fields.Char("Server Port")
    batch1_destination = fields.Char("Destination/ Url")
    batch1_aggretation_level = fields.Selection([
        ('5 miniutes', '5 miniutes'),
        ('15 miniutes', '15 miniutes'),
        ('30 miniutes', '30 miniutes'),
        ('60 miniutes', '60 miniutes'),
    ], "Aggretation Level")
    batch1_delivery_format = fields.Selection(
        string=u'Delivery Fromat',
        selection=[('xml', 'xml'), ('pipe delimited', 'pipe delimited')])

    batch1_delivery_schdule = fields.Selection(
        string=u'Delivery Schedule',
        selection=[('15 miniutes', '15 miniutes'), ('Hourly', 'Hourly'),
                   ('Daily', 'Daily')])
    batch1_enable_encryption = fields.Boolean("Enable Encryption")
    batch1_sni_host_name = fields.Char("SNI Host Name")
    ### Batch 2###
    batch2_enable = fields.Boolean("Enable Batch 2")
    batch2_server_url = fields.Char("Server Address")
    batch2_server_port = fields.Char("Server Port")
    batch2_destination = fields.Char("Destination/ Url")
    batch2_aggretation_level = fields.Selection([
        ('5 miniutes', '5 miniutes'),
        ('15 miniutes', '15 miniutes'),
        ('30 miniutes', '30 miniutes'),
        ('60 miniutes', '60 miniutes'),
    ], "Aggretation Level")
    batch2_delivery_format = fields.Selection(
        string=u'Delivery Fromat',
        selection=[('xml', 'xml'), ('pipe delimited', 'pipe delimited')])

    batch2_delivery_schdule = fields.Selection(
        string=u'Delivery Schedule',
        selection=[('15 miniutes', '15 miniutes'), ('Hourly', 'Hourly'),
                   ('Daily', 'Daily')])
    batch2_enable_encryption = fields.Boolean("Enable Encryption")
    batch2_sni_host_name = fields.Char("SNI Host Name")

    ### Real Time ###
    real_time_enable = fields.Boolean("Enable Real Time")
    real_time_server_url = fields.Char("Server Address")
    real_time_server_port = fields.Char("Server Port")
    real_time_destination = fields.Char("Destination/ Url")
    real_time_delivery_protocol = fields.Selection([('vli', 'VLI'),
                                                    ('http', 'HTTP')],
                                                   "Delivery Protocol")
    real_time_delivery_frequency = fields.Integer("Delivery Frequency (in ms)")
    real_time_skip_inactivity = fields.Boolean("Skip Inactivity")

    # def _compute_format_count(self):
    #     self.file_format_count = len(
    #         self.env['htc.site_file_format_type'].search([('site_id', '=',
    #                                                        self.id)]))

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = record.site_name
            result.append((record.id, name))
        return result

    @api.one
    @api.depends('file_name_format_ids', 'file_name_separator')
    def get_file_name(self):
        name_list = []
        if self.file_name_format_ids:
            file_symbol_list = self.env['htc.site_file_format_type'].search(
                [('site_id', '=', self.id), ('status', '=', True)],
                order='file_name_format_order, id, name')
            for file_symbol in file_symbol_list:
                if file_symbol.format_type == "Member":
                    if file_symbol.value != 'mac_address':
                        name_list.append(self[file_symbol.value])
                    else:
                        name_list.append('xx:xx:xx:xx:xx:xx')
                if file_symbol.format_type == "Date":
                    name_list.append(
                        str(datetime.datetime.today().strftime(
                            file_symbol.value)))
                if file_symbol.format_type == "Time":
                    name_list.append(
                        str(datetime.datetime.today().strftime(
                            file_symbol.value)))
            self.site_file_name_format = (
                self.file_name_separator.join(name_list)) + ".xml"

    @api.model
    def create(self, values):
        enable_ftp = values.get('ftp_enable', False)
        enable_email = values.get('email_enable', False)
        enable_batch1 = values.get('batch1_enable', False)
        enable_batch2 = values.get('batch2_enable', False)
        enable_real_time = values.get('real_time_enable', False)
        if enable_ftp is False:
            for key in list(
                    filter(lambda x: x.startswith('ftp'), values.keys())):
                values[key] = None
        if enable_email is False:
            for key in list(
                    filter(lambda x: x.startswith('email'), values.keys())):
                values[key] = None
        if enable_batch1 is False:
            for key in list(
                    filter(lambda x: x.startswith('batch1'), values.keys())):
                values[key] = None
        if enable_batch2 is False:
            for key in list(
                    filter(lambda x: x.startswith('batch2'), values.keys())):
                values[key] = None
        if enable_real_time is False:
            for key in list(
                    filter(lambda x: x.startswith('real_time'), values.keys())):
                values[key] = None

        record = super(Site, self).create(values)
        return record

    def _mapName(x, y):
        return y[0]

    @api.multi
    def write(self, values):
        enable_ftp = values.get('ftp_enable', False)
        enable_email = values.get('email_enable', False)
        enable_batch1 = values.get('batch1_enable', False)
        enable_batch2 = values.get('batch2_enable', False)
        enable_real_time = values.get('real_time_enable', False)
        if enable_ftp is False:
            for name in list(
                    filter(lambda x: x.startswith('ftp'),
                           list(map(self._mapName, self._fields.items())))):
                values.update({name: False})
        if enable_email is False:
            for name in list(
                    filter(lambda x: x.startswith('email'),
                           list(map(self._mapName, self._fields.items())))):
                values.update({name: False})
        if enable_batch1 is False:
            for name in list(
                    filter(lambda x: x.startswith('batch1'),
                           list(map(self._mapName, self._fields.items())))):
                values.update({name: False})
        if enable_batch2 is False:
            for name in list(
                    filter(lambda x: x.startswith('batch2'),
                           list(map(self._mapName, self._fields.items())))):
                values.update({name: False})
        if enable_real_time is False:
            for name in list(
                    filter(lambda x: x.startswith('real_time'),
                           list(map(self._mapName, self._fields.items())))):
                values.update({name: False})

        record = super(Site, self).write(values)
        return record

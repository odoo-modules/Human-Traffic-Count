# -*- coding: utf-8 -*-
from odoo import api, fields, models
import datetime


class Sensor(models.Model):
    _name = 'htc.sensor'
    _inherit = 'mail.thread'
    key = 'z@nd0Techn010Gy'

    site_group_id = fields.Many2one(
        "htc.site.group", "Site Group", required=True)
    mac_address = fields.Char("Mac Address", required=True)
    xml_format = fields.Selection([('Xml 1', 'Xml 1'), ('Xml 2', 'Xml 2'),
                                   ('Latest', 'Latest')],
                                  string="XML Format",
                                  default='Latest',
                                  required=True)
    device_name = fields.Char("Device Name")
    division_id = fields.Char("Division Id", default="")
    sensor_id = fields.Char("Sensor Id", default="")
    sensor_name = fields.Char("Sensor Name", default="")
    hardware_release_version = fields.Char(
        "Hardware Release Version", default="")
    serial_number = fields.Char("Serial Number", default="")
    software_release = fields.Char("Software Version", default="")
    host_name = fields.Char("Host Name", default="")
    ip_address = fields.Char("IP Address")
    sensor_site_ids = fields.One2many("htc.sensor.sites", "sensor_id",
                                      "Sensor_Site")
    # site_code = fields.Char(compute="get_site", store=False, string="Site")
    site_id = fields.Many2one(
        "htc.site", "Site", store=False, compute="get_site")
    status = fields.Boolean("Active/Inactive")
    group_sensor_ids = fields.One2many(
        "htc.group_sensors", "sensor_id", string="Group")

    import_date = fields.Date('Imported Date')
    ref_file_name = fields.Char('Imported File Name')
    company_code = fields.Char('Company Code')
    invoice_no = fields.Char('Invoice No')
    invoice_date = fields.Char('Invoice Date')
    brand_name = fields.Char('Brand Name')
    license_code = fields.Char('License Code')
    template_file_name = fields.Char(
        'Template Name', store=False, compute='_get_template_name')

    # in_status = fields.Selection([
    #     (5, 'Sensor In'),
    #     (10, 'Sensor Out'),
    # ],
    #                              required=False,
    #                              store=False,
    #                              readonly=False,
    #                              default=5,
    #                              compute="get_in_status")
    # out_status = fields.Integer(
    #     "Group Out Status",
    #     required=False,
    #     store=False,
    #     default=10,
    #     readonly=False)
    # enable_alert = fields.Boolean(
    #     "Enable Alert",
    #     compute='get_enable_alert',
    #     default=False,
    #     readonly=False,
    #     store=False,
    # )
    # process_count = fields.Integer("Process Count", default=1, store=False)
    # current_counter_date = fields.Date(
    #     'Current Counter Date',
    #     required=True,
    #     store=False,
    #     default=datetime.datetime(1990, 1, 1).date())
    # inform_limit_count = fields.Integer(
    #     "Limit to Inform",
    #     compute='get_inform_limit_count',
    #     store=False,
    #     default=10,
    #     readonly=False,
    #     required=False)

    # @api.one
    # @api.depends('in_status')
    # def get_in_status(self):
    #     param_name = str(self.env.uid) + '_' + 'group_id_global'
    #     group_id_global = self.env['ir.config_parameter'].sudo().get_param(
    #         param_name)
    #     if group_id_global and self.group_sensor_ids:
    #         group_id_global = int(group_id_global)
    #         if group_id_global in map(lambda x: x.group_id.id,
    #                                   self.group_sensor_ids):
    #             for gs in self.group_sensor_ids:
    #                 if gs.group_id.id == group_id_global:
    #                     self.in_status = gs.in_status
    #         else:
    #             self.in_status = 5
    #             self.out_status = 10
    #     else:
    #         if self.in_status:
    #             if self.in_status == 10:
    #                 self.out_status = 5
    #             else:
    #                 self.in_status = 5
    #                 self.out_status = 10
    #         else:
    #             self.in_status = 5
    #             self.out_status = 10

    # @api.one
    # @api.depends('enable_alert')
    # def get_enable_alert(self):
    #     param_name = str(self.env.uid) + '_' + 'group_id_global'
    #     group_id_global = self.env['ir.config_parameter'].sudo().get_param(
    #         param_name)
    #     if group_id_global and self.group_sensor_ids:
    #         group_id_global = int(group_id_global)
    #         if group_id_global in map(lambda x: x.group_id.id,
    #                                   self.group_sensor_ids):
    #             for gs in self.group_sensor_ids:
    #                 if gs.group_id.id == group_id_global:
    #                     self.enable_alert = gs.enable_alert
    #         else:
    #             self.enable_alert = False
    #     else:
    #         if self.enable_alert:
    #             self.enable_alert = True
    #         else:
    #             self.enable_alert = False

    # @api.one
    # @api.depends('inform_limit_count')
    # def get_inform_limit_count(self):
    # param_name = str(self.env.uid) + '_' + 'group_id_global'
    # group_id_global = self.env['ir.config_parameter'].sudo().get_param(
    #     param_name)
    # if group_id_global and self.group_sensor_ids:
    #     group_id_global = int(group_id_global)
    #     if group_id_global in map(lambda x: x.group_id.id,
    #                               self.group_sensor_ids):
    #         for gs in self.group_sensor_ids:
    #             if gs.group_id.id == group_id_global:
    #                 self.inform_limit_count = gs.inform_limit_count
    #     else:
    #         self.inform_limit_count = 0
    # else:
    #     if not self.inform_limit_count:
    #         self.inform_limit_count = 0
    #     else:
    #         self.inform_limit_count = self.inform_limit_count

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            mac_address = record.mac_address
            if record.device_name:
                mac_address = record.device_name + " " + mac_address
            result.append((record.id, mac_address))
        return result

    @api.multi
    def _get_template_name(self):
        result = []
        for record in self:
            if record.sensor_site_ids:
                if len(record.sensor_site_ids) > 1:
                    for v in record.sensor_site_ids:
                        if v.status is True:
                            record.template_file_name = v.file_name_field_template_id.template_name
                else:
                    for v in record.sensor_site_ids:
                        record.template_file_name = v.file_name_field_template_id.template_name

    @api.one
    @api.depends('sensor_site_ids')
    def get_site(self):
        for ssi in self.mapped('sensor_site_ids'):
            if ssi.status is True:
                for record in self:
                    # record.site_code = ssi.site_id.site_code
                    record.site_id = ssi.site_id

    @api.one
    @api.depends('group_sensor_ids')
    def get_status(self):
        for gs in self.mapped('group_sensor_ids'):
            if gs.sensor_id == self.id:
                for record in self:
                    record.in_status = gs.in_status
                    record.out_status = gs.out_status
                    record.inform_limit_count = gs.inform_limit_count
                    record.enable_alert = gs.enable_alert

    def toggle_status(self):
        record = super(Sensor, self).write({'status': not self.status})
        return record

    # @api.one
    # @api.depends('sensor_site_ids')
    # def get_site(self):
    #     for ssi in self.mapped('sensor_site_ids'):
    #         if ssi.status is True:
    #             for record in self:
    #                 # record.site_code = ssi.site_id.site_code
    #                 record.site_id = ssi.site_id

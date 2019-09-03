# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models
import inspect
from . import site


class SiteGroup(models.Model):
    _name = 'htc.site.group'
    _inherit = 'mail.thread'

    site_group_name = fields.Char(
        "Site Group Name", required=True, help="Please key in site group name")
    site_group_code = fields.Char(
        "Site Group Code", required=True, help="Please key in site group code", size=4)
    license_code = fields.Char(
        "License Code", required=True, help="Please key in license no.")
    sensor_ids = fields.One2many("htc.sensor", "site_group_id", "Sensors")
    site_ids = fields.One2many("htc.site", "site_group_id", "Sites")
    _sql_constraints = [('site_group_code_unique', 'unique(site_group_code)',
                         "Can't be duplicate value for Site Group Code!")]
    site_count = fields.Integer(
        '# Sites',
        compute='_compute_site_count',
        help="The number of sites under this site group (Does not consider the children sensors)"
    )

    sensor_count = fields.Integer(
        '# Sensors',
        compute='_compute_sensor_count',
        help="The number of sites under this site group (Does not consider the children sensors)"
    )

    file_name_field_ids = fields.One2many(
        "htc.file_name_field_template",
        "site_group_id",
        string="File Name Template")

    file_name_field_temp_count = fields.Integer(
        '# Format Count',
        compute='_compute_file_name_field_count',
        help="The file format of site")

    def _compute_site_count(self):
        self.site_count = len(self.env['htc.site'].search([('site_group_id',
                                                            '=', self.id)]))

    def _compute_sensor_count(self):
        self.sensor_count = len(self.env['htc.sensor'].search([('site_group_id',
                                                                '=', self.id)]))

    def _compute_file_name_field_count(self):
        self.file_name_field_temp_count = len(
            self.env['htc.file_name_field_template'].search([('site_group_id',
                                                              '=', self.id)]))

    # def sites_by_site_group_id(self):
    #     sites = self.mapped('site_ids')
    #     id = self.env.context.get('site_group_id')
    #     action = self.env.ref('htc.action_site_search_form').read()[0]
    #     action['context'] = {'search_default_site_group_id': id}
    #     return action

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
            code = record.site_group_name
            result.append((record.id, code))
        return result

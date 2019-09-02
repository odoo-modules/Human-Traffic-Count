from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date


class HtcSiteGroup(models.TransientModel):
    _name = "htc.site.group.wizard"

    @api.model
    def default_site_group(self):
        active_id = self._context.get('active_ids')[0]
        site_group_ids = self.env['htc.site.group'].browse(int(active_id))
        return site_group_ids.id

    name = fields.Char("Name", default="New")
    site_group_id = fields.Many2one(
        "htc.site.group", default=default_site_group, store=True)
    site_id = fields.Many2one("htc.site", "Site", required=True)

    file_name_field_template_id = fields.Many2one(
        "htc.file_name_field_template", "File Name Template", required=True)

    sensor_ids = fields.Many2many("htc.sensor", string="Sensors")

    @api.onchange('site_group_id')
    def onchange_site_group_id(self):
        domain = {}
        site = []
        print("hello")
        if not self.site_id:
            site_ids = self.env['htc.site'].search([('site_group_id', '=',
                                                     self.site_group_id.id)])
            for se in site_ids:
                site.append(se.id)
            domain = {'site_id': [('id', 'in', site)]}
        return {'domain': domain}

    @api.onchange('site_id')
    def onchange_site_id(self):
        self.sensor_ids = []
        self.file_name_field_template_id = None
        domain = {}
        if self.site_id:
            sensor = []
            sensors = self.env['htc.sensor'].search([
                ('site_group_id', '=', self.site_id.site_group_id.id)
            ])
            template_ids = self.site_id.file_name_field_template_ids
            for s in sensors:
                sensor.append(s.id)
            # domain = {'sensor_ids': [('id', 'in', sensor)]}
            sensor_ids = self.env['htc.sensor'].search([('id', 'in', sensor)])
            domain_ids = []
            for s in sensor_ids:
                if s.site_id.id is False:
                    domain_ids.append(s.id)

            domain = {
                'sensor_ids': [('id', 'in', domain_ids)],
                'file_name_field_template_id': [('id', 'in', template_ids.ids)]
            }
        return {'domain': domain}

    @api.model
    def create(self, vals):
        site_id = None
        sensor_obj = self.env['htc.sensor']
        sensor_site_obj = self.env['htc.sensor.sites']
        site_obj = self.env['htc.site']
        if vals['sensor_ids'][0][2]:
            for sensor in vals['sensor_ids'][0][2]:
                for sen in self.env['htc.sensor'].browse(sensor):
                    site_id = vals['site_id']
                    sensor_site_ids = sensor_site_obj.search([('sensor_id', '=',
                                                               sen.id)])
                    # sensor_sites = sensor_site_ids.filtered(
                    #     lambda r: r.site_id.id != site_id)
                    # sensor_site = sensor_site_ids.filtered(
                    #     lambda r: r.site_id.id == site_id)
                    # if sensor_sites:
                    #     for sesi in sensor_sites:
                    #         if sesi.status is True:
                    #             val = {
                    #                 'end_date': date.today(),
                    #                 'status': False,
                    #             }
                    #             sensor_sites.write(val)
                    # if sensor_site:
                    #     for sesi in sensor_site:
                    #         if sesi.status is False:
                    #             val = {
                    #                 'end_date': None,
                    #                 'status': True,
                    #             }
                    #             sensor_site.write(val)
                    # else:
                    val = {
                        'sensor_id': sen.id,
                        'site_id': site_id,
                        'start_date': date.today(),
                        'status': True,
                    }
                    sensor_site_obj.create(val)
                    sen.file_name_field_template_id = vals[
                        'file_name_field_template_id']
                    sensor_obj.write(sen)

        else:
            raise UserError(_("Please select sensor for site setting."))
        return super(HtcSiteGroup, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals['site_id']:
            for sen in self.sensor_ids:
                sen.site_id = vals['site_id']
        return super(HtcSiteGroup, self).write(vals)

from odoo import models,fields,api,_
from odoo.exceptions import UserError

class HtcSiteGroup(models.TransientModel):
    _name = "htc.site.group.wizard"

    name = fields.Char("Name", default="New")
    site_id = fields.Many2one("htc.site","Site", required=True)
    sensor_ids = fields.Many2many("htc.sensor", string="Sensors")

    @api.onchange('site_id')
    def onchange_site_id(self):
        self.sensor_ids = []
        domain = {}
        if self.site_id:
            sensor = []
            sensors = self.env['htc.sensor'].search([('sitegroup_id','=',self.site_id.site_group_id.id)])
            for s in sensors:
                sensor.append(s.id)
            domain = {'sensor_ids':[('id','in',sensor)]}
        return {'domain':domain}      

    @api.model
    def create(self, vals):
        if vals['sensor_ids'][0][2]:
            for sensor in vals['sensor_ids'][0][2]:
                for sen in self.env['htc.sensor'].browse(sensor):
                    sen.site_id= vals['site_id']
        else:
            raise UserError(_("Please select sensor for site setting."))
        return super(HtcSiteGroup, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals['site_id']:
            for sen in self.sensor_ids:
                sen.site_id= vals['site_id']
        return super(HtcSiteGroup, self).write(vals)
        
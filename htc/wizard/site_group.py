from odoo import models,fields,api,_
from odoo.exceptions import UserError,ValidationError
from datetime import date

class HtcSiteGroup(models.TransientModel):
    _name = "htc.site.group.wizard"

    @api.model
    def default_site_group(self):
        active_id = self._context.get('active_ids')[0]
        print ("Active",active_id)
        site_group_ids = self.env['htc.site.group'].browse(int(active_id))
        print ("group",site_group_ids)
        return site_group_ids.id

    name = fields.Char("Name", default="New")
    site_group_id = fields.Many2one("htc.site.group", default=default_site_group, store=True)
    site_id = fields.Many2one("htc.site","Site", required=True)
    sensor_ids = fields.Many2many("htc.sensor", string="Sensors")

    @api.onchange('site_group_id')
    def onchange_site_group_id(self):
        domain = {}
        site = []
        print("hello")
        if not self.site_id:
            site_ids = self.env['htc.site'].search([('site_group_id','=',self.site_group_id.id)])
            for se in site_ids:
                site.append(se.id)
            domain = {'site_id':[('id','in',site)]}
            print(domain)
        return{'domain':domain}

    @api.onchange('site_id')
    def onchange_site_id(self):
        self.sensor_ids = []
        domain = {}
        if self.site_id:
            sensor = []
            sensors = self.env['htc.sensor'].search([('site_group_id','=',self.site_id.site_group_id.id)])
            for s in sensors:
                sensor.append(s.id)
            domain = {'sensor_ids':[('id','in',sensor)]}
        return {'domain':domain}      

    @api.model
    def create(self, vals):
        site_id = None
        sensor_site_obj = self.env['htc.sensor.sites']
        site_obj = self.env['htc.site']
        if vals['sensor_ids'][0][2]:
            for sensor in vals['sensor_ids'][0][2]:
                for sen in self.env['htc.sensor'].browse(sensor):
                    site_id = vals['site_id']
                    sensor_site_ids = sensor_site_obj.search([('sensor_id','=',sen.id)])
                    if sensor_site_ids:
                        test1 =sensor_site_ids.filtered(lambda r: r.site_id.id != site_id)
                        for sesi in test1:
                            if sesi.status == True:
                                val = {
                                    'end_date': date.today(),
                                    'status': False,
                                    }
                                sensor_site_ids.write(val)
                        test =sensor_site_ids.filtered(lambda r: r.site_id.id == site_id)
                        for sesi in test:
                            if sesi.status == False:
                                val = {
                                    'end_date': None,
                                    'status': True,
                                    }
                                sensor_site_ids.write(val)
                        # elif sensor_site_ids:
                        #     if sensor_site_ids.status == False:  
                        #         val = {
                        #             'end_date': None,
                        #             'status': True,
                        #         }
                        #         sensor_site_ids.write(val)
                    else:
                        val = {
                            'sensor_id':sen.id,
                            'site_id': site_id,
                            'start_date':date.today(),
                            'status':True,
                        }
                        sensor_site_obj.create(val)

        else:
            raise UserError(_("Please select sensor for site setting."))
        return super(HtcSiteGroup, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals['site_id']:
            for sen in self.sensor_ids:
                sen.site_id= vals['site_id']
        return super(HtcSiteGroup, self).write(vals)
        
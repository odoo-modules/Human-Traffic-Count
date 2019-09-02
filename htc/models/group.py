# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models
import datetime


class Group(models.Model):
    _name = 'htc.group'
    _inherit = 'mail.thread'
    name = fields.Char("Group Name", required=True)
    code = fields.Char("Group Code", required=True)
    site_id = fields.Many2one("htc.site", string="Site", requierd=True)
    group_sensor_ids = fields.One2many(
        'htc.group_sensors', "group_id", string="Group Sensors")

    # sensor_ids = fields.Many2many(
    #     'htc.sensor',
    #     string='Sensors',
    #     store=False,
    #     readonly=False,
    #     compute="get_sensors")
    # compute="get_sensors"

    @api.onchange('code')
    def do_stuff(self):
        if self.code:
            self.name = str(self.name).upper()
        else:
            self.name = ""

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = record.name
            result.append((record.id, name))
        return result

        # @api.multi
        # def write(self, values):

        #     today = datetime.datetime.today()
        #     addlist = []
        #     senids = []
        #     value_sensor_ids = []
        #     operation_count = 0
        #     value_sensor_ids_len = 0
        #     value_sensors = values.get('sensor_ids')
        #     if value_sensors:
        #         value_sensor_ids = value_sensors[0][2]
        #         value_sensor_ids_len = len(value_sensor_ids)

        #     orgin_record = self.env['htc.group_sensors'].search([("group_id", "=",
        #                                                           self.id)])

        #     for ol_rec in orgin_record:
        #         senids.append(ol_rec.sensor_id.id)

        #     # searching delete records and delete them ###
        #     if value_sensor_ids and len(value_sensor_ids) > 0:
        #         diff_sen_ids = set(value_sensor_ids).symmetric_difference(
        #             set(senids))
        #         for diff_sen_id in diff_sen_ids:
        #             record_sensor = self.env['htc.group_sensors'].search([
        #                 ("group_id", "=", self.id), ('sensor_id', '=', diff_sen_id)
        #             ])
        #             if record_sensor:
        #                 # remove delete record #
        #                 record_sensor.unlink()
        #     else:
        #         if orgin_record:
        #             orgin_record.unlink()

        #     if value_sensor_ids and not len(value_sensors) > 1:
        #         for s_id in value_sensor_ids:
        #             db_record = self.env['htc.group_sensors'].search([
        #                 ('sensor_id', '=', s_id), ('group_id', '=', self.id)
        #             ])
        #             if not db_record:
        #                 addlist.append({
        #                     'group_id': self.id,
        #                     'sensor_id': s_id,
        #                     'in_status': 5,
        #                     'out_status': 10,
        #                     'enable_alert': False,
        #                     'inform_limit_count': 0,
        #                     'process_count': 1,
        #                     'current_counter_date': today
        #                 })
        #             else:
        #                 operation_count += 1
        #     else:
        #         if value_sensors:
        #             for i in range(len(value_sensors)):
        #                 if i == 0:
        #                     continue
        #                 db_record = self.env['htc.group_sensors'].search([
        #                     '&', ('sensor_id', '=', value_sensors[i][1]),
        #                     ('group_id', '=', self.id)
        #                 ])
        #                 temp = {
        #                     'id': db_record.id,
        #                     'group_id': self.id,
        #                     'sensor_id': value_sensors[i][1],
        #                     'in_status': 5,
        #                     'out_status': 10,
        #                     'enable_alert': False,
        #                     'inform_limit_count': 0,
        #                     'process_count': 1,
        #                     'current_counter_date': today
        #                 }
        #                 value = value_sensors[i][2]
        #                 # Merging dictionary ###
        #                 temp.update(value)
        #                 if temp.get('in_status') == 5:
        #                     temp['out_status'] = 10
        #                 else:
        #                     temp['out_status'] = 5
        #                 if not db_record:
        #                     addlist.append(temp)
        #                 else:
        #                     operation_count += 1
        #                     if value.get('in_status'):
        #                         if value.get('in_status') == 5:
        #                             value['out_status'] = 10
        #                         else:
        #                             value['out_status'] = 5
        #                     db_record.write(value)
        #     # remove duplicate items #
        #     addlist = [dict(t) for t in {tuple(d.items()) for d in addlist}]
        #     self.env['htc.group_sensors'].create(addlist)
        #     is_equal_operation_count = False
        #     if addlist:
        #         is_equal_operation_count = (operation_count +
        #                                     len(addlist)) == value_sensor_ids_len
        #     # Need to add extra more ###
        #     else:
        #         is_equal_operation_count = operation_count == value_sensor_ids_len
        #     if not is_equal_operation_count:
        #         need_to_adds = []
        #         addlist_sensor_id = map(lambda x: x.get('sensor_id'), addlist)
        #         need_to_add_ids = set(value_sensor_ids).symmetric_difference(
        #             set(addlist_sensor_id))
        #         for s_id in need_to_add_ids:
        #             db_record = self.env['htc.group_sensors'].search([
        #                 ('sensor_id', '=', s_id), ('group_id', '=', self.id)
        #             ])
        #             if not db_record:
        #                 temp = {
        #                     'id': db_record.id,
        #                     'group_id': self.id,
        #                     'sensor_id': s_id,
        #                     'in_status': 5,
        #                     'out_status': 10,
        #                     'enable_alert': False,
        #                     'inform_limit_count': 0,
        #                     'process_count': 1,
        #                     'current_counter_date': today
        #                 }
        #                 need_to_adds.append(temp)
        #         self.env['htc.group_sensors'].create(need_to_adds)

        # @api.one
        # @api.depends('group_sensor_ids')
        # def get_sensors(self):
        mlist = []
        list = []
        global_id = None
        param_name = str(self.env.uid) + '_' + 'group_id_global'

        self.env['ir.config_parameter'].sudo().set_param(param_name, global_id)
        record_set = None
        for gs in self.mapped('group_sensor_ids'):
            global_id = gs.group_id.id
            list.append(gs.sensor_id.id)
        sensors = self.env['htc.sensor'].search([("id", "in", list)])
        sensors = self.env['htc.sensor'].browse(list)

        for gs in self.mapped('group_sensor_ids'):
            for sensor in sensors:
                if sensor.id == gs.sensor_id.id:
                    sensor.in_status = gs.in_status
                    sensor.gs_id = gs.id
                    sensor.enable_alert = gs.enable_alert
                    sensor.inform_limit_count = gs.inform_limit_count
                    mlist.append(sensor)
        self.env['ir.config_parameter'].sudo().set_param(param_name, global_id)

        self.sensor_ids = sensors

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from docutils.nodes import field
from odoo import api, fields, models
import datetime


class GroupSensors(models.Model):
    _name = 'htc.group_sensors'
    _inherit = 'mail.thread'

    group_id = fields.Many2one("htc.group", string="Group", requierd=True)
    sensor_id = fields.Many2one("htc.sensor", string="Sensor", requierd=True)
    in_status = fields.Selection([
        (5, 'Sensor In'),
        (10, 'Sensor Out'),
    ],
                                 required=True,
                                 default=5)
    out_status = fields.Integer("Group Out Status", required=True, default=10)
    enable_alert = fields.Boolean("Enable Alert", default=False)
    process_count = fields.Integer("Process Count", default=1)
    current_counter_date = fields.Date('Current Counter Date',
                                       required=True,
                                       default=datetime.datetime(1990, 1,
                                                                 1).date())
    inform_limit_count = fields.Integer("Limit to Inform", default=0)
    _sql_constraints = [('group_sensors_unique', 'unique(group_id,sensor_id)',
                         "Can't be duplicate value for  Group and Sensor!")]

    @api.onchange('in_status')
    def do_stuff(self):
        if self.in_status:
            if self.in_status == 10:
                self.out_status = 5
            else:
                self.in_status = 5
                self.out_status = 10
        else:
            self.in_status = 5
            self.out_status = 10

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            gp_sensor_description = record.group_id.code + '-' + record.sensor_id.mac_address
            result.append((record.id, gp_sensor_description))
        return result

    @api.model
    def do_notify(self, status, total):
        return self.search([('enable_alert', '=', True)]).notify(status, total)

    @api.multi
    def notify(self, status, total):
        if status == 5:
            self.env['htc.notification_email'].email_notify(
                self, total, 'In', self.inform_limit_count)
        else:
            self.env['htc.notification_email'].email_notify(
                self, total, 'Out', self.inform_limit_count)

    # @api.multi
    # def notify(self):
    #     records = self.env['htc.group_sensors'].search([])
    #     for record in records:
    #         for sensor in record.sensor_id:
    #             for dailyCount in sensor.daily_counter_ids:
    #                 if record.current_counter_date < dailyCount.transaction_date:
    #                     record.process_count = 1
    #                     if record.in_status == 5 \
    #                             and dailyCount.daily_total_in > record.inform_limit_count * record.process_count:
    #                         # record.process_count += 1
    #                         # self.mail_message()
    #                         while dailyCount.daily_total_in > record.inform_limit_count * record.process_count:
    #                             record.process_count += 1
    #                             self.env[
    #                                 'htc.notification_email'].email_notify(
    #                                     record, dailyCount.daily_total_in,
    #                                     'In', record.inform_limit_count)
    #                             # self.mail_message(dailyCount.daily_total_in,record,self._cr,self._uid,self.ids,self._context)
    #                     elif record.in_status == 10 \
    #                             and dailyCount.daily_total_out > record.inform_limit_count * record.process_count:
    #                         # record.process_count += 1
    #                         # self.mail_message(dailyCount.daily_total_out,record,self._cr,self._uid,self.ids,self._context)
    #                         while dailyCount.daily_total_out > record.inform_limit_count * record.process_count:
    #                             record.process_count += 1
    #                             self.env[
    #                                 'htc.notification_email'].email_notify(
    #                                     record, dailyCount.daily_total_ou,
    #                                     'Out', record.inform_limit_count)
    #                             # self.mail_message(dailyCount.daily_total_out,record,self._cr,self._uid,self.ids,self._context)
    #                             # self, count, record, cr, uid, ids, context = None

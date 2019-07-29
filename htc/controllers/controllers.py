# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import Response
import datetime
import logging
import ipaddress
_logger = logging.getLogger(__name__)


class Htc(http.Controller):
    @http.route('/htc/getsensor/', auth='public', type='json', csrf=False)
    def list(self, **kw):
        try:
            data = kw.get('data', False)
            mac_address = data.get('mac_address')
            file_name = data.get('file_name')
            sensor = http.request.env['htc.sensor'].search(
                [("mac_address", "=", mac_address)], limit=1)
            if (sensor.id > 0):
                http.Response.status = "200"
                http.Response.content_type = 'application/json'
                return sensor
            else:
                http.Response.content_type = 'application/json'
                http.Response.status = "200"
                return None
        except Exception as e:
            _logger.error("Error seraching sensor with Mac-Address %s in %s ",
                          mac_address, file_name)
            http.Response.status = "400"
            http.Response.content_type = 'application/json'
            return None

    @http.route('/htc/transactions/',
                auth='public',
                methods=['POST'],
                type='json',
                csrf=False)
    def object(self, **kw):
        try:
            data = kw.get('data', False)
            first_obj = data[0]
            file_name = first_obj.get('file_name')
            device_name = first_obj.get('device_name')
            device_id = first_obj.get('device_id')
            host_name = first_obj.get('host_name')
            sensor_id = first_obj.get('sensor_id')
            site_id = first_obj.get('site_id')
            ip_address = first_obj.get('ip_address')
            timezone_name = first_obj.get('timezone_name')
            software_version = first_obj.get('software_version')
            serial_number = first_obj.get('serial_number')
            sensor_name = first_obj.get('name')
            mac_address = first_obj.get('mac_address')

            sensor = http.request.env['htc.sensor'].search(
                [("mac_address", "=", mac_address)], limit=1)
            site = http.request.env['htc.site'].search(
                [("site_code", "=", site_id)], limit=1)
            ipList = list(ipaddress.ip_network(site.ip_range, False).hosts())
            extract_ip_list = list(map(lambda x: x.compressed, ipList))

            valid_ip = list(filter(lambda x: x == ip_address, extract_ip_list))
            if len(valid_ip) > 0:
                date_string = data[0].get('transaction_date').split('T')[0]
                day = datetime.datetime.strptime(date_string, '%Y-%m-%d')
                # dt = datetime.datetime.strptime(date_string, '%Y-%m')
                week = day.isocalendar()[1]
                dayNumber = day.weekday()
                for obj in data:
                    http.request.env['htc.sensor_transaction'].create({
                        'site_id':
                        site.id,
                        'sensor_id':
                        obj.get('sensor_id'),
                        'transaction_date':
                        obj.get('transaction_date'),
                        'in_count':
                        obj.get('in_count'),
                        'out_count':
                        obj.get('out_count'),
                        'status':
                        obj.get('status'),
                        'process_count':
                        0,
                        'week':
                        week,
                        'day':
                        dayNumber,
                        'method':
                        obj.get('method'),
                        'start_time':
                        obj.get('start_time'),
                        'end_time':
                        obj.get('start_time')
                    })

                sensor.ip_address = ip_address
                sensor.device_name = device_name
                sensor.device_id = device_id
                sensor.host_name = host_name
                sensor.timezone_name = timezone_name
                sensor.software_release = software_version
                sensor.serial_number = serial_number
                sensor.sensor_name = sensor_name
            else:
                _logger.error("Invalid IP Address Range in %s",
                              file_name,
                              exc_info=1)
                http.Response.status = "400"
                http.Response.content_type = "application/json"
                return "Application Error"
        except Exception as e:
            http.request.env['htc.sensor_transaction'].log_transaction_error(
                file_name)
            http.Response.status = "400"
            http.Response.content_type = 'application/json'
            return "system error"
        http.Response.status = '200'
        http.Response.content_type = 'application/json'
        return "successfully inserted"

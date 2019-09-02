from odoo import models, fields, api, _
from datetime import datetime
from io import StringIO
import base64
import xlrd
from xlrd import open_workbook
from odoo.exceptions import UserError, ValidationError
import os
import csv

header_fields = ['Mac Address', 'XML Format']

header_indexes = {}


class ImportSiteGroup(models.Model):
    _name = 'import.site_group'
    _inherit = 'mail.thread'

    import_fname = fields.Char('Filename', size=128)
    # import_file = fields.Binary('File', required=True)
    import_file = fields.Binary('File')

    err_log = ''
    enable_debug_log = fields.Boolean('Debug Log Enable', default=True)

    # Read data and import to database ##########
    def import_data(self):
        file_data = []
        val = {}
        header_line = True
        active_id = active = None
        sensor_site_obj = self.env['htc.sensor.sites']
        site_obj = self.env['htc.site']
        sensor_obj = self.env['htc.sensor']
        site_group_obj = self.env['htc.site.group']
        active_id = self._context.get('current_id')
        active = site_group_obj.browse(int(active_id))
        val['site_group_name'] = active.site_group_name
        val['site_group_code'] = active.site_group_code
        val['license_code'] = active.license_code
        site_group_id = site_group_obj.search([('site_group_code', '=',
                                                val['site_group_code'])])
        if not site_group_id:
            site_group_id = site_group_obj.create(val).id
        import_file = self.import_file
        file_name = self.import_fname
        r = []
        if file_name and file_name.find('.csv') != -1:
            date_time_obj = datetime.strptime(
                file_name.split('_')[0], '%d%m%y%H%M%S')
            if date_time_obj and file_name.split('_')[1] == 'sensor' and file_name.split('_')[2] == 'import.csv':
                lines = base64.decodestring(import_file).decode('utf-8').split(
                    '\r\n')
                if len(lines) <= 4:
                    raise ValidationError(_("Invalid File Content"))
                    return True
                count = 0
                for line in lines:
                    count += 1
                    if line != "" and count < 4:
                        if line.find(':') == -1:
                            raise ValidationError(_("Invalid File Content"))
                            return True
                        cols = line.split(":")
                        file_data.append(cols)
                    if line != "" and count >= 4:
                        if line.find(',') == -1:
                            raise ValidationError(_("Invalid File Content"))
                            return True
                        cols = line.split(",")
                        file_data.append(cols)

                sen_val = {}
                sensor_ids = None
                sensors_with_group = []
                site_group = []
                sensors = []
                count = 0
                already_sensor_count = 0
                for data in file_data[4:]:
                    sensor_id = sensor_obj.search(
                        [('mac_address', 'ilike', data[0])], limit=1)
                    if sensor_id:
                        self.env['ir.logging'].create({
                            'create_uid':
                                self.env.uid,
                            'create_date':
                                datetime.today(),
                            'name':
                                "import data",
                            'type':
                                "client",
                            'dbname':
                                self.env.cr.dbname,
                            'path':
                                "",
                            'func':
                                "import sensor",
                            'line':
                                "",
                            'level':
                                "ERROR",
                            'message':
                                'Already sersor import with Mac-Address - {1} with file name {0}'
                                .format(sensor_id[0].ref_file_name, data[0])
                        })
                        already_sensor_count += 1
                        continue
                    else:
                        sen_val = {
                            'mac_address': data[0],
                            'brand_name': data[1],
                            'serial_number': data[2],
                            'license_code': data[3],
                            'site_group_id': site_group_id.id,
                            'xml_format': 'Latest',
                            'import_date': datetime.now().date(),
                            'ref_file_name': file_name,
                            'status': True,
                            'company_code': file_data[0][1],
                            'invoice_no': file_data[1][1],
                            'invoice_date': file_data[2][1],
                        }
                    sensor_obj.create(sen_val)
                    if self.enable_debug_log:
                        self.env['ir.logging'].create({
                            'create_uid':
                                self.env.uid,
                            'create_date':
                                datetime.today(),
                            'name':
                                "import data",
                            'type':
                                "client",
                            'dbname':
                                self.env.cr.dbname,
                            'path':
                                "",
                            'func':
                                "import sensor",
                            'line':
                                "",
                            'level':
                                "Info",
                            'message':
                                'sersor successful imported with Mac-Address - {1} with file name {0}'
                                .format(sen_val.get('ref_file_name'), sen_val.get('mac_address'))
                        })

                if self.enable_debug_log is False:
                    self.env['ir.logging'].create({
                        'create_uid':
                            self.env.uid,
                        'create_date':
                            datetime.today(),
                        'name':
                            "import data",
                        'type':
                            "client",
                        'dbname':
                            self.env.cr.dbname,
                        'path':
                            "",
                        'func':
                            "import sensor",
                        'line':
                            "",
                        'level':
                            "Info",
                        'message':
                            'Total Sensor Count - {2} and imported sensor count {1} and file name {0}'
                            .format(
                                str(len(file_data[4:])),
                                str(len(file_data[4:]) - already_sensor_count),
                                file_name)
                    })
            else:
                self.env['ir.logging'].create({
                    'create_uid': self.env.uid,
                    'create_date': datetime.today(),
                    'name': "import data",
                    'type': "client",
                    'dbname': self.env.cr.dbname,
                    'path': "",
                    'func': "import sensor",
                    'line': "",
                    'level': "Error",
                    'message': 'Invalid file Name format'
                })
        else:
            self.env['ir.logging'].create({
                'create_uid': self.env.uid,
                'create_date': datetime.today(),
                'name': "import data",
                'type': "client",
                'dbname': self.env.cr.dbname,
                'path': "",
                'func': "import sensor",
                'line': "",
                'level': "Error",
                'message': 'File is required to upload'
            })
            raise ValidationError(_("Please choose file to import."))
            return True

    @api.one
    def _get_template(self):
        directory_path = os.getcwd()
        file_path = directory_path + '\\static\\csv\\sensor_import.csv'
        self.import_template = base64.b64encode(open(file_path, "rb").read())

    import_template = fields.Binary(
        'Template', compute="_get_template", store=False)

    @api.multi
    def get_import_template(self):
        file_name = datetime.now().strftime(
            '%d%m%y%H%M%S') + '_sensor_import.csv'
        url = f'/web/content/import.site_group/{self.id}/import_template/{file_name}?download=true'

        return {'type': 'ir.actions.act_url', 'name': 'contract', 'url': url}

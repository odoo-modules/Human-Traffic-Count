from odoo import models, fields, api, _
from datetime import datetime
from io import StringIO
import base64
import xlrd
from xlrd import open_workbook
from odoo.exceptions import UserError, ValidationError

header_fields = ['Mac Address', 'XML Format']

header_indexes = {}


class ImportSiteGroup(models.Model):
    _name = 'import.site_group'
    _inherit = 'mail.thread'

    import_fname = fields.Char('Filename', size=128)
    import_file = fields.Binary('File', required=True)

    err_log = ''

    def _check_file_ext(self):
        for import_file in self:
            if '.dat' or '.DAT' or '.xls' or '.xlsx' in import_file.import_fname:
                return True
            else:
                return False
        return True

    _constraints = [(_check_file_ext, "Please import EXCEL file!",
                     ['import_fname'])]

    # ## Load excel data file
    def get_excel_datas(self, sheets):
        result = []
        for s in sheets:
            cell_row = 0
            for row in range(cell_row, s.nrows):
                values = []
                for col in range(0, s.ncols):
                    values.append(s.cell(row, col).value)
                result.append(values)
        return result

    # ## Check excel row headers with header_fields and define header indexes for database fields
    def get_headers(self, line):
        print("line=>", line[0].strip())
        if line[0].strip() not in header_fields:

            raise ValidationError(
                _('Error :'),
                _("Error while processing the header line %s.\\n\nPlease check your Excel separator as well as the column header fields"
                  ) % line)
        else:
            # ## set header_fields to header_index with value -1
            for header in header_fields:
                header_indexes[header] = -1

            col_count = 0
            for ind in range(len(line)):
                if line[ind] == '':
                    col_count = ind
                    break
                elif ind == len(line) - 1:
                    col_count = ind + 1
                    break

            for i in range(col_count):
                header = line[i].strip().lower()
                if header not in header_fields:
                    self.err_log += '\n' + _(
                        "Invalid Excel File, Header Field '%s' is not supported !"
                    ) % header
                else:
                    header_indexes[header] = i

            for header in header_fields:
                if header_indexes[header] < 0:
                    self.err_log += '\n' + _(
                        "Invalid Excel file, Header '%s' is missing !") % header

    ######### Read data and import to database ##########
    def import_data(self):
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
        print("site_groupw1=>", site_group_id)
        import_file = self.import_file
        file_name = self.import_fname
        print("file name", file_name)
        r = []
        if file_name.find('.xls') != -1 or file_name.find('.xlsx') != -1:
            lines = base64.decodestring(import_file)
            print("lines", lines)
            wb = open_workbook(file_contents=lines)
            r = self.get_excel_datas(wb.sheets())
        all_data = []
        created_counnt = 0
        updated_count = 0
        skipped_count = 0
        skip_data = []
        for ln in r:
            if not ln or ln and ln[0] and ln[0][0] in ['', '#']:
                continue
            if header_line:
                self.get_headers(ln)
                header_line = False
            else:
                if ln and ln[0] and ln[0][0] not in ['#', '']:
                    import_vals = {}
                    import_vals['Mac Address'] = ln[0]
                    import_vals['XML Format'] = ln[1]
                    all_data.append(import_vals)
                    print("DATA", all_data)
            if all_data:
                sen_val = {}
                sensor_ids = None
                sensors_with_group = []
                sensors = []
                for data in all_data:
                    sensors_with_group = []
                    sensors = []
                    print('------------')
                    excel_row = all_data.index(data) + 2
                    print('excel row => ' + str(excel_row))
                    print('data ' + str(data))
                    print(data)
                    mac_address = data['Mac Address']
                    xml_format = data['XML Format']
                    if mac_address and xml_format:
                        sensor_ids = sensor_obj.search([
                            ('mac_address', 'ilike', mac_address),
                            ('site_group_id', '=', site_group_id.id)
                        ])
                        sensors_with_group.append(sensor_ids.mac_address)
                    sensor_id = sensor_obj.search([('mac_address', 'ilike',
                                                    mac_address)])
                    if sensor_id:
                        for s in sensor_id:
                            sensors = []
                            print("s", s)
                            sensors.append(s.mac_address)
                            print("mac address", s.mac_address)
                if sensors_with_group != [False]:
                    raise ValidationError(
                        _("Please 'Inactive' the sensors of Mac Address %s .")
                        % sensors_with_group)
                else:
                    print("sens", sensors)
                    if sensors != []:
                        raise ValidationError(
                            _("Import Sensor already exit check the sensors of Mac Address %s ."
                              ) % sensors)
                    else:
                        sen_val = {
                            'mac_address': mac_address,
                            'xml_format': xml_format,
                            'site_group_id': site_group_id.id,
                        }
                        sensor_obj.create(sen_val)
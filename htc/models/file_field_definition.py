from odoo import api, fields, models, _
import datetime
from odoo.exceptions import ValidationError, RedirectWarning, UserError


class FileFieldDefinition(models.Model):
    _name = 'htc.file_field_definition'
    _inherit = 'mail.thread'
    _order = 'code_description, id'
    selection_list = [('site_name', 'Site Name'), ('site_code', 'Site Id'),
                      ('mac_address', 'Mac Address'),
                      ('%y%m%d', 'Count Data Date'),
                      ('%H%M%S', 'Last Count Time')]
    # format_type = fields.Selection(
    #     [
    #         ('Member', 'Member'),
    #         ('Date', 'Date'),
    #         ('Time', 'Time'),
    #     ],
    #     required=True,
    #     store=True,
    #     default=None,
    # )
    code_description = fields.Char(
        "Code Description", required=True, help="Key in Code Description")
    code = fields.Char("Code", required=True, help="Key in Code")
    map_to = fields.Selection(
        selection_list, required=True, help="Select Map To")
    # site_group_id = fields.Many2one(
    #     "htc.site.group", "Site Group", required=True)

    # status = fields.Boolean("Active", default=True)

    # brand_name = fields.Char(
    #     "Brand Name", required=True, help="Key in Brand Name")

    # def toggle_status(self):
    #     record = super(SiteGroupFileFieldDefinition,
    #                    self).write({'status': not self.status})
    #     return record

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = record.code + '-' + record.code_description
            result.append((record.id, name))
        return result

    # @api.multi
    # def write(self, values):
    #     check_list = ['format_type', 'value']
    #     result_value = values.get('value')
    #     format_type = values.get('format_type')
    #     if result_value is not None or format_type is not None:
    #         if result_value is None:
    #             result_value = self.value
    #         if format_type is None:
    #             format_type = self.format_type
    #         if format_type == 'Member':
    #             field_list = []
    #             for name, field in self.env['htc.site']._fields.items():
    #                 if not name.startswith('_') and not name.startswith(
    #                         'ftp'
    #                 ) and not name.startswith('email') and not name.startswith(
    #                         'batch'
    #                 ) and not name.startswith(
    #                         'real_time'
    #                 ) and name != 'display_name' and name != 'site_file_name_format' and name != 'interface_code' and name != 'ip_range' and isinstance(
    #                         field, (fields.Char)):
    #                     field_list.append(name)
    #             for name, field in self.env['htc.sensor']._fields.items():
    #                 if name == 'mac_address' and isinstance(field, (fields.Char)):
    #                     field_list.append(name)
    #             if field_list.count(result_value) == 0:
    #                 raise ValidationError(_("You cannot define  of 'Format Type = Member' as " + result_value + ". Value/ Format must be on of these 'Site Name' and 'Site Code'"))
    #                 return True
    #         if format_type == 'Date':
    #             field_list = ['%d%m%y', '%d%m%Y', '%y%m%d', '%Y%m%d']
    #             if field_list.count(result_value) == 0:
    #                 raise ValidationError(_("You cannot define  of 'Format Type = Date' as " + result_value + ". Value/ Format must be on of these 'dd-mm-yy', 'dd-mm-yyyy', 'yy-mm-dd', 'yyyy-mm-dd'"))
    #                 return True
    #         if format_type == 'Time':
    #             field_list = ['%H%M%S']
    #             if field_list.count(result_value) == 0:
    #                 raise ValidationError(_("You cannot define  of 'Format Type = Time' as " + result_value + ". Value/ Format must be on of these 'HH:MM:SS'"))
    #                 return True
    #     super(SiteGroupFileFieldDefinition, self).write(values)
    #     return True

    # @api.model
    # def create(self, values):
    #     result = values.get('value')
    #     if values.get('format_type') == 'Member':
    #         field_list = []
    #         for name, field in self.env['htc.site']._fields.items():
    #             if not name.startswith('_') and not name.startswith(
    #                     'ftp'
    #             ) and not name.startswith('email') and not name.startswith(
    #                     'batch'
    #             ) and not name.startswith(
    #                     'real_time'
    #             ) and name != 'display_name' and name != 'site_file_name_format' and name != 'interface_code' and name != 'ip_range' and isinstance(
    #                     field, (fields.Char)):
    #                 field_list.append(name)
    #         for name, field in self.env['htc.sensor']._fields.items():
    #             if name == 'mac_address' and isinstance(field, (fields.Char)):
    #                 field_list.append(name)
    #         if field_list.count(result) == 0:
    #             raise ValidationError(_("You cannot define  of 'Format Type = Member' as " + values.get('value') + ". Value/ Format must be on of these 'Site Name' and 'Site Code'"))
    #             return True
    #     if values.get('format_type') == 'Date':
    #         field_list = ['%d%m%y', '%d%m%Y', '%y%m%d', '%Y%m%d']
    #         if field_list.count(result) == 0:
    #             raise ValidationError(_("You cannot define  of 'Format Type = Date' as " + values.get('value') + ". Value/ Format must be on of these 'dd-mm-yy', 'dd-mm-yyyy', 'yy-mm-dd', 'yyyy-mm-dd'"))
    #             return True
    #     if values.get('format_type') == 'Time':
    #         field_list = ['%H%M%S']
    #         if field_list.count(result) == 0:
    #             raise ValidationError(_("You cannot define  of 'Format Type = Time' as " + values.get('value') + ". Value/ Format must be on of these 'HH:MM:SS'"))
    #             return True
    #     record = super(SiteGroupFileFieldDefinition, self).create(values)
    #     return record

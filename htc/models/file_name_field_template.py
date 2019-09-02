from odoo import api, fields, models, _
import datetime
from odoo.exceptions import ValidationError, RedirectWarning, UserError


class FileNameFieldTemplate(models.Model):
    _name = 'htc.file_name_field_template'
    _inherit = 'mail.thread'
    template_name = fields.Char(
        "Template Name", required=True, help="Key in Template Name")
    file_fields_definition_ids = fields.Many2many(
        'htc.file_field_definition',
        string='File Field Definition',
        required=True)
    file_name_separator = fields.Selection([('.', 'dot (.)'),
                                            ('_', 'underscore (_)')],
                                           default='.')
    status = fields.Boolean("Active/Inactive", default=True)

    symbol_file_format = fields.Char(
        "Sample File Format", store=False, compute="_get_symbol_file_format")

    site_group_id = fields.Many2one(
        'htc.site.group', string='Site Group', required=True)

    template_code = fields.Char(
        "Template Code",
        help="Auto Generate Template Code",
        store=True,
        compute="_get_template_code")

    remark = fields.Char("Remark", help="Key in Remark", store=True)

    def toggle_status(self):
        record = super(FileNameFieldTemplate,
                       self).write({'status': not self.status})
        return record

    @api.model
    @api.depends('file_fields_definition_ids', 'file_name_separator')
    def _get_symbol_file_format(self):
        list = []
        for x in self.file_fields_definition_ids:
            list.append(x.code)
        self.symbol_file_format = self.file_name_separator.join(
            str(x) for x in list)
        self.symbol_file_format += '.xml'

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = record.template_code
            result.append((record.id, name))
        return result

    @api.model
    @api.depends('site_group_id')
    def _get_template_code(self):
        list = []
        if self.site_group_id and self.template_code is False:
            site_group_code = self.site_group_id.site_group_code
            list.append(site_group_code)
            year = datetime.datetime.today().strftime("%y")
            list.append(year)
            count = len(self.env['htc.file_name_field_template'].search([
                ('site_group_id', '=', self.site_group_id.id)
            ]))

            serial = '{0:03}'.format(count + 1)

            list.append(serial)
            self.template_code = '-'.join(str(x) for x in list)

    @api.multi
    def browse_site_group(self):
        aa = 'b'
        compose_form = self.env.ref('htc.action_site_group_search_form', False)
        compose_form.context = {'search_default_id': self.site_group_id.id}
        return {
            'name': compose_form.name,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': compose_form.res_model,
            'search_view': compose_form.search_view,
            'views': [(False, 'form')],
            'view_id': compose_form.view_id.id,
            # 'target': 'new',
            'context': compose_form.context
        }

    @api.multi
    def get_site_group_name(self):
        return self.site_group_id.site_group_name

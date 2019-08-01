from odoo import api, fields, models
from odoo import SUPERUSER_ID


class NotificationEmail(models.Model):
    _name = 'htc.notification_email'
    _inherit = "res.partner"

    @api.multi
    def email_notify(self, record, total, types, limit_count, device_name):
        domain = [('name', 'ilike', 'HTC Notify')]
        to_emails = []
        process_count = record['inform_limit_count']
        user_name = partner = None
        template = self.env['mail.template'].search(domain, limit=1)
        for temp in template:
            temp_id = temp.id
        if template:
            template.email_from = temp.email_to = email = users = None
            email = self.env['ir.mail_server'].search([("active", "=", True)])
            users = self.env['res.users'].search([])
            if email:
                template.email_from = email.smtp_user
            if users:
                for user in users:
                    if user.enable_notify_count is True:
                        if not user_name:
                            user_name = user.partner_id.display_name
                        if not partner:
                            partner = user.partner_id.id
                            template.partner_to = partner
                        to_emails.append(user.partner_id.email)
            if len(to_emails) > 0:
                template.emial_to = to_emails[0]
                to_emails.pop()
            if len(to_emails) > 0:
                template.email_cc = ','.join(to_emails)
            template.subject = str("Notafication for " + str(device_name))
            template.body_html = str(
                'Dear ' + str(user_name) +
                ',<br/><br/>We provide notification for ' + str(device_name) +
                '.<br/>Total count : ' + str(total) +
                '<br/>Informed Count : ' + str(process_count) +
                '<br/>Always inform after next ' + str(limit_count) + '.<br/>')
            template.send_mail(temp_id, True)
            return True
        else:
            return False


class MailTemplate(models.Model):
    _inherit = "mail.template"

    device_id = fields.Char("Device ID", store=False)
    count_type = fields.Char("Count Type", store=False)
    total_count = fields.Integer("Total Count", store=False)
    process_count = fields.Integer("Inform Count", store=False)
    process_limit_count = fields.Integer("Limit Count", store=False)


class Users(models.Model):
    _inherit = "res.users"

    enable_notify_count = fields.Boolean("Enable Notify Count?", default=False,store=True)


class Message(models.Model):
    _inherit = 'mail.message'

    @api.model
    def _get_record_name(self, values):
        """ Return the related document name, using name_get. It is done using
            SUPERUSER_ID, to be sure to have the record name correctly stored. """
        print("values", values)
        model = values.get('model', self.env.context.get('default_model'))
        res_id = values.get('res_id', self.env.context.get('default_res_id'))
        if not model or not res_id or model not in self.env:
            return False
        print('MAIL MSG', self.env[model].sudo().browse(res_id).name_get()[0][1])
        return self.env[model].sudo().browse(res_id).name_get()[0][1]
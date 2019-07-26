from odoo import api, fields, models
from odoo import SUPERUSER_ID


class NotificationEmail(models.Model):
    _name = 'htc.notification_email'
    _inherit = "res.partner"

    @api.multi
    def email_notify(self, record,total,types,limit_count):
        # domain = [('name', 'ilike', 'HTC Mail_For_Count_2')]
        # domain_server = [('name', 'ilike', 'notification')]
        # template = self.env['mail.template'].search(domain, limit=1)
        # mail_server = self.env['ir.mail_server'].search(domain_server, limit=1)
        # users = self.env['res.partner'].search([])
        # user = users[0]
        # su_id = self.env['res.partner'].browse(SUPERUSER_ID)
        # # self.parent_id = user
        # for temp in template:
        #     temp_id = temp.id
        # if template:
        #     template.mail_server_id = mail_server.id
        #     values = template.generate_email(temp_id)
        #     values['email_from'] = su_id.email
        #     values['res_id'] = False
        #     mail_mail_obj = self.env['mail.mail']
        #     values['mail_server_id'] = mail_server.id
        #     # values['mail_message_id'] = 98
        #     # values['res_id'] = 0
        #     msg_id = mail_mail_obj.create(values)
        #     if msg_id:
        #         mail_mail_obj.send(msg_id)
        #     # generate_email
        #     # template.mail_message_id = 98
        #     # template.send_mail(temp_id, True)
        #     return True
        # else:
        #     return False
        domain = [('name', 'ilike', 'HTC Notify')]
        to_emails=[]
        process_count = record.process_count
        device_id = record.sensor_id.device_id
        user_name = partner = None
        # .['sensor'].device_id
        template = self.env['mail.template'].search(domain, limit=1)
        for temp in template:
            temp_id = temp.id
            if temp_id:
                temp1 = 0
            temp1 += 1
        if template:
            # template.process_count = record.process_count
            # template.inform_count = record.inform_limit_count
            # template.email_from="aungmyoswe@zandotech.com"
            # template.email_to="yarkyawsoe@zandotech.com"
            template.email_from = temp.email_to = email = users = None
            template.subject = "Notify HTC for NN" + str(device_id)
            email = self.env['ir.mail_server'].search([])
            users = self.env['res.users'].search([])
            if email:
                template.email_from = email.smtp_user
            if users:
                for user in users:
                    if user.enable_notify_count == True:
                        if not user_name:
                            user_name = user.partner_id.display_name
                        if not partner:
                            partner = user.partner_id.id
                            template.partner_to = partner
                        to_emails.append(user.partner_id.email)
            template.emial_to=to_emails[0]
            to_emails.pop()
            # template.email_cc = ','.join(to_emails)
            template.device_id = device_id
            template.count_type = types
            template.process_count = process_count
            template.process_limit_count = limit_count
            template.body_html =str('Dear'+str(user_name)+',<br/><br/>We provide notification for '+str(device_id)+'.<br/>Total count : '+str(total)+'<br/>Informed Count : '+ str(process_count)+'<br/>Always inform after next '+str(limit_count)+'.<br/>')
            template.send_mail(temp1, True)
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

    enable_notify_count = fields.Boolean("Enable Notify Count?", default=False, store=True)

class Message(models.Model):
    _inherit = 'mail.message'

    @api.model
    def _get_record_name(self, values):
        """ Return the related document name, using name_get. It is done using
            SUPERUSER_ID, to be sure to have the record name correctly stored. """
        print ("values", values)
        model = values.get('model', self.env.context.get('default_model'))
        res_id = values.get('res_id', self.env.context.get('default_res_id'))
        if not model or not res_id or model not in self.env:
            return False
        print ('MAIL MSG', self.env[model].sudo().browse(res_id).name_get()[0][1])
        return self.env[model].sudo().browse(res_id).name_get()[0][1]
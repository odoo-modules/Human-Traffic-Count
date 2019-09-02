# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'HTC',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Human Traffic Count',
    'depends': ['base', 'web', 'mail', 'contacts'],
    'data': [
        'security/ir.model.access.csv', 'views/site_group_tree_views.xml',
        'views/file_field_definition_views.xml',
        'views/import_site_group_view.xml', 'wizard/site_group_issue_view.xml',
        'views/file_name_field_template_views.xml',
        'views/site_group_views.xml', 'views/ir_logging_view.xml',
        'views/actions.xml', 'views/sensor_views.xml', 'views/site_views.xml',
        'views/group_views.xml', 'views/group_sensors_views.xml',
        'data/noti_email_views.xml', 'views/sensor_transaction_views.xml',
        'views/sensor_site_views.xml'
    ],
    'demo': [],
    'css': [],
    'images': ['images/screen.png'],
    'installable': True,
    'auto_install': False,
    'application': True,
}

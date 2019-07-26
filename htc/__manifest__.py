# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name'          : 'HTC',
    'version'       : '1.0',
    'category'      : 'Tools',
    'summary'       : 'Human Traffic Count',
    'depends'       : ['base','web', 'mail', 'contacts'],
    'data'          : [
        'security/ir.model.access.csv',
        'data/actions.xml',
        'data/sensor_views.xml',
        'data/site_views.xml',
        'data/group_views.xml',
        'wizard/site_group_issue_view.xml',
        'data/site_group_views.xml',
        'data/group_sensors_views.xml',
        'data/noti_email_views.xml',
        'data/noti_email_2_views.xml',
        'views/views.xml',
    ],
    'demo'          : [
    ],
    'css'           : [],
    'images'        :[
        'images/screen.png'
    ],
    'installable'   : True,
    'auto_install'  : False,
    'application'   : True,
}

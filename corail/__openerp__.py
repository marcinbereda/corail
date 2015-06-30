# -*- coding: utf-8 -*-

{
    'name' : 'Corail - service',
    'version' : '1.0',
    'author' : 'Marcin Bereda',
    'category' : '',
    'description' : """
    CORAIL Service
    """,
    'website': '',
    'depends' : ['mail'],
    'data': [
             'security/corail_security.xml',
             'security/ir.model.access.csv',
             
             'view/res_partner_view.xml',
             'view/c_device_view.xml',
             'view/c_task_view.xml',
             
             'view/portal_view.xml'
    ],
    'qweb' : [
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

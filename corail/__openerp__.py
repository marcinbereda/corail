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
    'depends' : ['mail','portal'],
    'data': [
             'security/corail_security.xml',
             'security/ir.model.access.csv',
             
             'wizard/c_motohour_wizard_view.xml',
             'wizard/c_flaw2task_view.xml',
             
             'view/res_partner_view.xml',
             'view/c_device_view.xml',
             'view/c_task_view.xml',
             'view/c_offer_view.xml',
             
             'view/portal_view.xml',
             
             'view/c_task_workflow.xml',
             'view/c_offer_workflow.xml',
             'view/c_device_workflow.xml',
             'view/c_empty_view.xml',
             
             'view/webclient_templates.xml',
             'view/menu_view.xml'
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

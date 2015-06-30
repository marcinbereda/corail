# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning

import datetime
import pdb

Device_State = [
    ('used','Używane'),
    ('unused','Nieużywane')
]

class c_device(models.Model):
    _name = "c.device"
    _description = "Urządzenie"
    _inherit = ['mail.thread']
    
    name = fields.Char(string='Nazwa', required=True)
    partner_id = fields.Many2one('res.partner', string='Klient', domain=[('customer', '=', 'True'),('is_company','=',True)])
    serial_number = fields.Char(string='Numer seryjny')
    date_delivery = fields.Date(string='Data dostawy')
    warranty_start = fields.Date(string='Gwarancja od')
    warranty_stop = fields.Date(string='Gwaracncja do')
    motohours = fields.Float(string='Przepracowane motogodziny')
    state = fields.Selection(Device_State, string='Jest używane', default='used')
    attachment_ids = fields.Many2many('ir.attachment', 'c_device_attachment_rel', 'c_device_templ_id', 'attachment_id', string='Załączniki')
    task_ids = fields.One2many('c.task', 'device_id', string='Zadania')
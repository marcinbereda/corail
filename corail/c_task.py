# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning

import datetime
import pdb

Task_State = [
    ('scheduled','Zaplanowane'),
    ('done','Wykonane'),
    ('cancelled','Anulowane')
]

Performs = [
    ('client','Klient'),
    ('corail','CORAIL')
]

class c_task(models.Model):
    _name = "c.task"
    _description = "Zadanie"
    _inherit = ['mail.thread']
    
    name = fields.Char(string='Opis', required=True)
    device_id = fields.Many2one('c.device', string='Urządzenie', required=True)
    partner_id = fields.Many2one('res.partner', string='Klient', domain=[('customer', '=', 'True'),('is_company','=',True)], required=True)
    date_start = fields.Datetime(string='Data rozpoczęcia', required=True)
    date_stop = fields.Datetime(string='Data zakończenia', required=True)
    state = fields.Selection(Task_State, string='Status', default='scheduled', required=True, readonly=True)
    performs = fields.Selection(Performs, string='Wykonuje', default='client', required=True)
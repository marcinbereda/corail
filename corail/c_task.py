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
    device_id = fields.Many2one('c.device', string='Urządzenie', required=True, domain="[('partner_id','=',partner_id)]")
    serial_number = fields.Char(string='Numer seryjny', related='device_id.serial_number', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Klient', domain=[('customer', '=', 'True'),('is_company','=',True)], required=True)
    date_start = fields.Datetime(string='Data rozpoczęcia', required=True)
    date_stop = fields.Datetime(string='Data zakończenia', required=True)
    state = fields.Selection(Task_State, string='Status', default='scheduled', required=True, readonly=True)
    performs = fields.Selection(Performs, string='Wykonuje', default='client', required=True)
    description = fields.Text(string='Procedura szczegółowa')
    
    manual_data = fields.Binary(string='Procedura szczegółowa')
    manual_name = fields.Char(string='Nazwa pliku')
    flaw_id = fields.Many2one('c.device.flaw', string='Usterka')
    
    @api.multi
    def cancel_flaw(self):
        if self.flaw_id:
            self.flaw_id.signal_workflow('close')
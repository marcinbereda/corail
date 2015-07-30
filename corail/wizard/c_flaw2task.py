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

class c_flaw2task(models.TransientModel):
    _name = "c.flaw2task"
    _description = "Usterka do zadania"
    
    name = fields.Char(string='Opis', required=True)
    device_id = fields.Many2one('c.device', string='Urządzenie', required=True, domain="[('partner_id','=',partner_id)]", readonly=True)
    serial_number = fields.Char(string='Numer seryjny', related='device_id.serial_number', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Klient', domain=[('customer', '=', 'True'),('is_company','=',True)], required=True, readonly=True)
    date_start = fields.Datetime(string='Data rozpoczęcia', required=True)
    date_stop = fields.Datetime(string='Data zakończenia', required=True)
    state = fields.Selection(Task_State, string='Status', default='scheduled', required=True, readonly=True)
    performs = fields.Selection(Performs, string='Wykonuje', default='client', required=True)
    description = fields.Text(string='Procedura szczegółowa')
    
    manual_data = fields.Binary(string='Procedura szczegółowa')
    manual_name = fields.Char(string='Nazwa pliku')
    
    def default_get(self, cr, uid, fields, context=None):
        if context is None: context = {}
        res = super(c_flaw2task, self).default_get(cr, uid, fields, context=context)
        flaw_id = context.get('active_id')
        flaw = self.pool.get('c.device.flaw').browse(cr, uid, flaw_id)
        
        res.update({'partner_id': flaw.partner_id.id,'device_id': flaw.device_id.id})
        return res
    
    @api.one
    def create_task(self):
        w = self.browse(self._ids)
        flaw_id = self.env['c.device.flaw'].browse(self._context['active_id'])
        
        value = {
                 'name': w.name,
                 'device_id': flaw_id.device_id.id,
                 'partner_id': flaw_id.partner_id.id,
                 'date_start': w.date_start,
                 'date_stop': w.date_stop,
                 'state': 'scheduled',
                 'performs': w.performs,
                 'description': w.description,
                 'manual_data': w.manual_data,
                 'manual_name': w.manual_name,
                 'flaw_id': flaw_id.id,
                 }
        
        
        task_id = self.env['c.task'].create(value)
        flaw_id.write({'task_id': task_id.id})
        
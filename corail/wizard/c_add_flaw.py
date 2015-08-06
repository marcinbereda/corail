# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning

import datetime
import pdb

Flaw_State = [
    ('new','Nowe'),
    ('in_progress','Rozpatrywane'),
    ('service','Serwis'),
    ('close','Zamknięte')
]

class c_add_flaw(models.TransientModel):
    _name = "c.add.flaw"
    _description = "Usterka"
    
    partner_id = fields.Many2one('res.partner', string='Klient', required=True, domain="[('customer', '=', 'True'),('is_company','=',True)]")
    device_id = fields.Many2one('c.device', string='Urządzenie', required=True, domain="[('partner_id', '=', partner_id)]")
    description = fields.Text(string='Opis usterki', required=True)
    attachment_ids = fields.Many2many('ir.attachment', 'c_device_flaw_attachment_rel', 'c_device_flaw_id', 'attachment_id', string='Załączniki')
    task_id = fields.Many2one('c.task', string='Zadanie')
    state = fields.Selection(Flaw_State, string='Status', default='new', track_visibility='onchange')
    
    def default_get(self, cr, uid, fields, context=None):
        if context is None: context = {}
        res = super(c_add_flaw, self).default_get(cr, uid, fields, context=context)
        
        user = self.pool.get('res.users').browse(cr, uid, uid)
        partner_id = user.partner_id.parent_id.id
        
        res.update({'partner_id': partner_id})
        return res
    
    @api.one
    def add_flaw(self):
        w = self.browse(self._ids)
        user = self.env['res.users'].browse(self._uid)
        partner_id = user.partner_id.parent_id.id
        
        flaw_obj = self.env['c.device.flaw']
        vals = {}
        vals = {
                'partner_id': partner_id or False,
                'device_id': w.device_id.id or False,
                'description': w.description,
                'state': 'new',
                }
        flaw_obj.create(vals)
        
        return True
        
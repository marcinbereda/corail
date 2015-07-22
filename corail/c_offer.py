# -*- coding: utf-8 -*-

from openerp import models, fields, api, tools, _
from openerp.exceptions import except_orm, Warning, RedirectWarning

from dateutil.relativedelta import relativedelta
from openerp import tools
import datetime
import calendar
import pdb

Offer_State = [
    ('draft','Zapytanie'),
    ('offer','Oferta'),
    ('accept','Akceptacja'),
    ('reject','Odrzucenie')
]

class c_offer(models.Model):
    _name = "c.offer"
    _description = "Oferta na urządzenie"
    _inherit = ['mail.thread']
    
    description = fields.Text(string='Opis urządzenia')
    partner_id = fields.Many2one('res.partner', string='Klient')
    state = fields.Selection(Offer_State, string='Status', default='draft')
    
    file_data = fields.Binary(string='Instrukcja obsługi i konserwacji')
    file_name = fields.Char(string='Nazwa pliku')
    
    attachment_ids = fields.Many2many('ir.attachment', 'c_offer_attachment_rel', 'c_offer_templ_id', 'attachment_id', string='Inne załączniki')
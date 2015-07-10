# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning

from dateutil.relativedelta import relativedelta
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
    
    @api.one
    def _get_motohours(self):
        if self.motohours_ids:
            self.add_motohours = True if (datetime.datetime.today()).date() >= datetime.datetime.strptime(self.motohours_ids[-1].create_date, '%Y-%m-%d %H:%M:%S').date()+relativedelta(days=7) else False
            self.motohours = self.motohours_ids[-1].hours
        else:
            self.motohours = 0.0
            self.add_motohours = True
    
    name = fields.Many2one('c.device.model', string='Nazwa', required=True)
    partner_id = fields.Many2one('res.partner', string='Klient', domain=[('customer', '=', 'True'),('is_company','=',True)])
    serial_number = fields.Char(string='Numer seryjny')
    date_delivery = fields.Date(string='Data dostawy')
    warranty_start = fields.Date(string='Gwarancja od')
    warranty_stop = fields.Date(string='Gwaracncja do')
    motohours = fields.Float(compute='_get_motohours', string='Przepracowane motogodziny', store=False)
    add_motohours = fields.Boolean(compute='_get_motohours', string='Dodanie motogodzin', store=False)
    rtime_id = fields.Many2one('c.device.response.time', string='Czas reakcji')
    #state = fields.Selection(Device_State, string='Jest używane', default='used')
    attachment_ids = fields.Many2many('ir.attachment', 'c_device_attachment_rel', 'c_device_templ_id', 'attachment_id', string='Załączniki')
    task_ids = fields.One2many('c.task', 'device_id', string='Zadania')
    motohours_ids = fields.One2many('c.device.motohours', 'device_id', string='Motogodziny')
    

class c_device_model(models.Model):
    _name = "c.device.model"
    _description = "Model urządzenia"
    
    name = fields.Char(string='Model')
    
class c_device_motohours(models.Model):
    _name = "c.device.motohours"
    _description = "Motogodziny urządzenia"
    
    hours = fields.Float(string='Motogodziny', required=True)
    create_date = fields.Datetime(string='Data dodania', readonly=True)
    create_uid = fields.Many2one('res.users', string='Dodał', readonly=True)
    device_id = fields.Many2one('c.device', string='Urządzenie', required=True)
    
    
Unit_Time = [
    ('hours','godziny'),
    ('day','dni')
]
class c_device_response_time(models.Model):
    _name = "c.device.response.time"
    _description = "Czas reakcji"
    
    name = fields.Integer(string='Ilość', required=True)
    unit = fields.Selection(Unit_Time, string='Jednostka', required=True)
    
    @api.multi
    def name_get(self):
        result = []
        Unit_Time = {
            'hours': 'godziny',
            'day': 'dni'
        }

        for rt in self:
            result.append((rt.id, "%s %s" % (rt.name, Unit_Time[rt.unit.encode('utf-8')])))
        return result
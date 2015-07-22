# -*- coding: utf-8 -*-

from openerp import models, fields, api, tools, _
from openerp.exceptions import except_orm, Warning, RedirectWarning

from dateutil.relativedelta import relativedelta
from openerp import tools
import datetime
import calendar
import pdb

Device_State = [
    ('used','Działa poprawnie'),
    ('unused','Zgłoszenie serwisowe')
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
            
    @api.one
    def _get_age_device(self):
        date_str = {
                    'year': ['rok', 'lata', 'lat'],
                    'month': ['m-c', 'm-ce', 'm-cy'],
                    'day': ['dzień', 'dni']
                    }
        
        if self.date_delivery:
            age = ''
            today = datetime.date.today()
            date_delivery = datetime.datetime.strptime(self.date_delivery, '%Y-%m-%d').date()

            years = today.year - date_delivery.year
            months = today.month - date_delivery.month
            days = today.day - date_delivery.day
            
            if days < 0:
                day_month = calendar.monthrange(date_delivery.year, date_delivery.month)[1]
                days = day_month + days
                months -= 1
                
            if months < 0:
                months = 12 + months
                years -= 1
                
            if years > 0:
                if years >= 5:
                    age += '%s %s '%(years, date_str['year'][2])
                elif years >= 2:
                    age += '%s %s '%(years, date_str['year'][1])
                else:
                    age += '%s %s '%(years, date_str['year'][0])
                
                if months > 0 and days > 0:
                    age += ', '
                elif months > 0 or days > 0:
                    age += ' i '
                    
            if months > 0:
                if months >= 5:
                    age += '%s %s '%(months, date_str['month'][2])
                elif months >= 2:
                    age += '%s %s '%(months, date_str['month'][1])
                else:
                    age += '%s %s '%(months, date_str['month'][0])
                    
                if days > 0:
                    age += ' i '
                    
            if days > 0:
                if days >= 2:
                    age += '%s %s '%(days, date_str['day'][1])
                else:
                    age += '%s %s '%(days, date_str['day'][0])
            self.age_device = age
    
    name = fields.Many2one('c.device.model', string='Nazwa', required=True)
    partner_id = fields.Many2one('res.partner', string='Klient', domain=[('customer', '=', 'True'),('is_company','=',True)], required=True)
    serial_number = fields.Char(string='Numer seryjny')
    date_delivery = fields.Date(string='Data odbioru')
    age_device = fields.Char(compute='_get_age_device', string='Wiek', store=False)
    warranty_stop = fields.Date(string='Gwaracncja do')
    motohours = fields.Float(compute='_get_motohours', string='Motogodziny', store=False)
    add_motohours = fields.Boolean(compute='_get_motohours', string='Dodanie motogodzin', store=False)
    rtime_id = fields.Many2one('c.device.response.time', string='Czas reakcji')
    state = fields.Selection(Device_State, string='Status', default='used')
    attachment_ids = fields.Many2many('ir.attachment', 'c_device_attachment_rel', 'c_device_templ_id', 'attachment_id', string='Załączniki')
    task_ids = fields.One2many('c.task', 'device_id', string='Zadania')
    motohours_ids = fields.One2many('c.device.motohours', 'device_id', string='Motogodziny')
    image = fields.Binary(string='Zdjęcie')
    
    description = fields.Text(string='Uwagi')
    location = fields.Text(string='Lokalizacja')
    
    category = fields.Char(string='Kategoria')
    purpose = fields.Char(string='Przeznaczenie')
    specifications = fields.Text(string='Charakretystyczne parametry techniczne')
    permissions = fields.Text(string='Wymagane uprawnienia')
    
    tecnical_doc_data = fields.Binary(string='Dokumentacja techniczno-ruchowa')
    tecnical_doc_name = fields.Char(string='Nazwa pliku')
    user_manual_data = fields.Binary(string='Instrukcja użytkownika')
    user_manual_name = fields.Char(string='Nazwa pliku')
    maint_manual_data = fields.Binary(string='Instrukcja konserwacji')
    maint_manual_name = fields.Char(string='Nazwa pliku')
    spare_parts_data = fields.Binary(string='Lista części zamiennych')
    spare_parts_name = fields.Char(string='Nazwa pliku')
    
    calendar_ids = fields.One2many('c.service.calendar', 'device_id', string='Kalendarz obsługowy')
    

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
    
Cycle = [
    ('month','miesiąc'),
    ('6month','6 miesięcy'),
    ('year','rok')
    ]
    
class c_service_calendar(models.Model):
    _name = "c.service.calendar"
    _description = "Kalendarz obsługowy"
    
    description = fields.Char(string='Opis')
    device_id = fields.Many2one('c.device', string='Urządzenie', required=True)
    cycle = fields.Selection(Cycle, string='Cykl', required=True)
    
    
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
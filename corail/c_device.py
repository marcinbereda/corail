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
    warranty_stop = fields.Date(string='Gwarancja do')
    motohours = fields.Float(compute='_get_motohours', string='Motogodziny', store=False)
    add_motohours = fields.Boolean(compute='_get_motohours', string='Dodanie motogodzin', store=False)
    rtime_id = fields.Many2one('c.device.response.time', string='Czas reakcji')
    state = fields.Selection(Device_State, string='Status', default='used')
    attachment_ids = fields.Many2many('ir.attachment', 'c_device_attachment_rel', 'c_device_templ_id', 'attachment_id', string='Załączniki')
    task_ids = fields.One2many('c.task', 'device_id', string='Zadania')
    motohours_ids = fields.One2many('c.device.motohours', 'device_id', string='Motogodziny')
    image = fields.Binary(string='Zdjęcie')
    user = fields.Many2one('res.partner', string='Osoba odpowiedzialna', domain="[('parent_id','=',partner_id)]")
    main_subdevice_id = fields.Many2one('c.subdevice', string='Nadrzędne urządzenie', required=True)
    subdevice_id = fields.Many2one('c.subdevice', string='Podrzędne urządzenie')
    
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
    
    category2 = fields.Char(string='Kategoria')
    purpose2 = fields.Char(string='Przeznaczenie')
    specifications2 = fields.Text(string='Charakretystyczne parametry techniczne')
    permissions2 = fields.Text(string='Wymagane uprawnienia')
    
    tecnical_doc_data2 = fields.Binary(string='Dokumentacja techniczno-ruchowa')
    tecnical_doc_name2 = fields.Char(string='Nazwa pliku')
    user_manual_data2 = fields.Binary(string='Instrukcja użytkownika')
    user_manual_name2 = fields.Char(string='Nazwa pliku')
    maint_manual_data2 = fields.Binary(string='Instrukcja konserwacji')
    maint_manual_name2 = fields.Char(string='Nazwa pliku')
    spare_parts_data2 = fields.Binary(string='Lista części zamiennych')
    spare_parts_name2 = fields.Char(string='Nazwa pliku')
    
    calendar_ids = fields.One2many('c.service.calendar', 'device_id', string='Kalendarz obsługowy')
    flaw_ids = fields.One2many('c.device.flaw', 'device_id', string='Zgłoszenia')
    
    @api.multi
    def onchange_main_subdevice(self, main_sub_id, subdevice_id):
        if not main_sub_id:
            return True
        
        sub_id = self.env['c.subdevice'].browse(main_sub_id)
        sub2_id = self.env['c.subdevice'].browse(subdevice_id)
        value = {}
        
        calendar = []
        for cal in sub_id.calendar_ids:
            calendar.append([0,False,{'cycle': cal.cycle, 'description': cal.description}])
        for cal2 in sub2_id.calendar_ids:
            calendar.append([0,False,{'cycle': cal2.cycle, 'description': cal2.description}])
        
        value = {
                 'image': sub_id.image or False,
                 'category': sub_id.category or '',
                 'purpose': sub_id.purpose or '',
                 'specifications': sub_id.specifications or '',
                 'permissions': sub_id.permissions or '',
                 
                 'tecnical_doc_data': sub_id.tecnical_doc_data or False,
                 'tecnical_doc_name': sub_id.tecnical_doc_name or '',
                 'user_manual_data': sub_id.user_manual_data or False,
                 'user_manual_name': sub_id.user_manual_name or '',
                 'maint_manual_data': sub_id.maint_manual_data or False,
                 'maint_manual_name': sub_id.maint_manual_name or '',
                 'spare_parts_data': sub_id.spare_parts_data or False,
                 'spare_parts_name': sub_id.spare_parts_name or '',
                 'calendar_ids': calendar
                 }

        return {'value': value}
    
    @api.multi
    def onchange_subdevice(self, main_sub_id, subdevice_id):
        if not subdevice_id:
            return True
        
        sub_id = self.env['c.subdevice'].browse(subdevice_id)
        sub2_id = self.env['c.subdevice'].browse(main_sub_id)
        value = {}
        
        calendar = []
        for cal in sub_id.calendar_ids:
            calendar.append([0,False,{'cycle': cal.cycle, 'description': cal.description}])
        for cal2 in sub2_id.calendar_ids:
            calendar.append([0,False,{'cycle': cal2.cycle, 'description': cal2.description}])
        
        value = {
                 'category2': sub_id.category or '',
                 'purpose2': sub_id.purpose or '',
                 'specifications2': sub_id.specifications or '',
                 'permissions2': sub_id.permissions or '',
                 
                 'tecnical_doc_data2': sub_id.tecnical_doc_data or False,
                 'tecnical_doc_name2': sub_id.tecnical_doc_name or '',
                 'user_manual_data2': sub_id.user_manual_data or False,
                 'user_manual_name2': sub_id.user_manual_name or '',
                 'maint_manual_data2': sub_id.maint_manual_data or False,
                 'maint_manual_name2': sub_id.maint_manual_name or '',
                 'spare_parts_data2': sub_id.spare_parts_data or False,
                 'spare_parts_name2': sub_id.spare_parts_name or '',
                 'calendar_ids': calendar
                 }

        return {'value': value}
    
    
class c_subdevice(models.Model):
    _name = "c.subdevice"
    _description = "Podurządzenie"
    _inherit = ['mail.thread']
    
    name = fields.Char(string='Model', required=True)
    image = fields.Binary(string='Zdjęcie')
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
    
    name = fields.Char(string='Model', required=True)
    
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
    
    description = fields.Char(string='Opis', required=True)
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
    
    
Flaw_State = [
    ('new','Nowe'),
    ('in_progress','Rozpatrywane'),
    ('service','Serwis'),
    ('close','Zamknięte')
]
    
class c_device_flaw(models.Model):
    _name = "c.device.flaw"
    _description = "Usterka"
    _inherit = ['mail.thread']
    _rec_name = 'device_id'
    
    partner_id = fields.Many2one('res.partner', string='Klient', required=True, domain="[('customer', '=', 'True'),('is_company','=',True)]")
    device_id = fields.Many2one('c.device', string='Urządzenie', required=True, domain="[('partner_id', '=', partner_id)]")
    description = fields.Text(string='Opis usterki', required=True)
    attachment_ids = fields.Many2many('ir.attachment', 'c_device_flaw_attachment_rel', 'c_device_flaw_id', 'attachment_id', string='Załączniki')
    task_id = fields.Many2one('c.task', string='Zadanie')
    state = fields.Selection(Flaw_State, string='Status', default='new', track_visibility='onchange')
    
    
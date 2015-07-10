# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning

import datetime
import pdb

Device_State = [
    ('used','Używane'),
    ('unused','Nieużywane')
]

class c_motohour_wizard(models.TransientModel):
    _name = "c.motohour.wizard"
    _description = "Motogodziny"
    
    hours = fields.Float(string='Ilość godzin', required=True)
    
    @api.one
    def add_motohour(self):
        w = self.browse(self._ids)
        device_id = self._context['active_id']
        device = self.env['c.device'].browse(device_id)
        
        if device.motohours > w.hours:
            raise except_orm(('Ostrzeżenie!'), ('Poprzedni wpis motogodzin jest większy od aktualnego'))
        
        
        self.env['c.device.motohours'].create({'device_id': device.id, 'hours': w.hours})
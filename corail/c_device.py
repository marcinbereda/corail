# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning

import datetime
import pdb

class c_device(models.Model):
    _name = "c.device"
    _description = "Urządzenie"
    _inherit = ['mail.thread']
    
    name = fields.Char(string='Nazwa', required=True)
# -*- coding: utf-8 -*-

from openerp import models, fields, api, _

class c_empty(models.Model):
    _name = "c.empty"
    _description = "Próbny"
    
    name = fields.Char(string='Nazwa', required=True)
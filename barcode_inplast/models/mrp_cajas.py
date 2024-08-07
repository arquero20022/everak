from odoo import models, fields

class MrpCajas(models.Model):
    _name = 'mrp.cajas'
    _description = 'Cajas in MRP'

    name = fields.Char(string='Caja Name', required=True)

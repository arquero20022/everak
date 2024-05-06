from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = 'res.company'

    pnt_goods_state_table = fields.Binary("State Table verification")

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    pnt_sale_report_id = fields.Many2one('ir.actions.report')
    pnt_invoice_report_id = fields.Many2one('ir.actions.report')
    pnt_picking_report_id = fields.Many2one('ir.actions.report', domain=[("binding_model_id", "=", "stock.picking")])
    pnt_label_box_type_id = fields.Many2one('ir.actions.report')
    pnt_label_pallet_type_id = fields.Many2one('ir.actions.report')

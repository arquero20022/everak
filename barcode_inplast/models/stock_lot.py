from odoo import models, fields, api



class StockLot(models.Model):
    _inherit = 'stock.lot'

    barcode_input = fields.Text(string="Barcode Input")

    processed_barcodes = fields.One2many('barcode.line', 'lot_id', string="Processed Barcodes")

    def process_barcodes(self):
        for record in self:
            if record.barcode_input:
                barcodes = record.barcode_input.split('\t')

                record.processed_barcodes = [(0, 0, {'barcode': bc}) for bc in barcodes]
                record.barcode_input = ''  # Limpiar el campo después de procesar las entradas


class BarcodeLine(models.Model):
    _name = 'barcode.line'
    _description = 'Barcode Line'

    lot_id = fields.Many2one('stock.lot', string="Lot/Serial Number")
    barcode = fields.Char(string="Barcode")

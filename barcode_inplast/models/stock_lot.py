from odoo import models, fields, api


class StockLot(models.Model):
    _inherit = 'stock.lot'

    ######### Fields #########
    # Campo para la entrada del código de barras
    pnt_barcode_input = fields.Text(string="Barcode Input")

    # Campo para almacenar los códigos de barras procesados
    pnt_processed_barcodes = fields.Many2many(
        'stock.lot', 'stock_lot_barcode_rel', 'lot_id', 'barcode_id',
        string="Processed Barcodes", help="Barcodes processed from the input"
    )

    # Campo para el sub producto principal
    pnt_sub_product_id = fields.Many2one(
        'product.template', string="Sub Product",
        domain="[('id', 'in', pnt_sub_product_ids)]"
    )

    # Campo para los sub productos disponibles
    pnt_sub_product_ids = fields.Many2many(
        'product.template', string="Available Sub Products",
        compute='_compute_pnt_sub_product_ids'
    )

    # Campo booleano que indica si se seleccionó un sub producto
    pnt_sub_product_selected = fields.Boolean(
        string="Sub Product Selected",
        compute='_compute_pnt_sub_product_selected',
        store=True
    )

    # Campo para el producto de origen
    pnt_originating_product_id = fields.Many2one('product.product', string="Originating Product",
                                             domain="[('id', '=', product_id)]")

    # Campo para el lote de origen
    pnt_originating_lot_id = fields.Many2one('stock.lot', string="Originating Lot",
                                         domain="[('product_id', '=', pnt_originating_product_id)]")

    ######### Compute Methods #########
    @api.depends('pnt_sub_product_id')
    def _compute_pnt_sub_product_selected(self):
        # Este método se ejecuta cada vez que el campo 'pnt_sub_product_id' cambia
        # y establece 'pnt_sub_product_selected' a True si 'pnt_sub_product_id' tiene un valor.
        for record in self:
            record.pnt_sub_product_selected = bool(record.pnt_sub_product_id)

    @api.depends('product_id')
    def _compute_pnt_sub_product_ids(self):
        # Este método se ejecuta cada vez que el campo 'product_id' cambia
        # y calcula los sub productos disponibles basándose en 'product_id'.
        for record in self:
            if record.product_id and record.product_id.pnt_parent_id:
                record.pnt_sub_product_ids = record.product_id.pnt_parent_id.pnt_packing_ids
            else:
                record.pnt_sub_product_ids = self.env['product.template'].browse([])

    ######### Onchange Methods #########
    @api.onchange('pnt_originating_product_id')
    def _onchange_pnt_originating_product_id(self):
        # Este método se ejecuta cuando 'pnt_originating_product_id' cambia
        # y establece el dominio para 'pnt_originating_lot_id'.
        for record in self:
            return {'domain': {'pnt_originating_lot_id': [('product_id', '=', record.pnt_originating_product_id.id)]}}

    @api.onchange('pnt_barcode_input')
    def _onchange_pnt_barcode_input(self):
        # Este método se ejecuta cada vez que 'pnt_barcode_input' cambia.
        for record in self:
            if record.pnt_barcode_input and record.pnt_sub_product_id:
                line = record.pnt_barcode_input
                lots, boxes = [], []

                if line:
                    # Divide la entrada del código de barras en lotes basados en 'MO'
                    lots = line.split('MO')
                    lots = [lot for lot in lots if lot]
                    for lot in lots:
                        lot_name = 'MO' + lot.strip()
                        # Busca si el lote ya existe
                        exist = self.env['stock.lot'].search(
                            [('product_id', '=', record.pnt_sub_product_id.id), ('name', '=', lot_name)])
                        if not exist:
                            # Si no existe, crea un nuevo lote
                            new_lot = self.env['stock.lot'].create({
                                'product_id': record.pnt_sub_product_id.id,
                                'name': lot_name,
                                'pnt_originating_product_id': record.product_id.id,
                                'pnt_originating_lot_id': record._origin.id
                            })
                            boxes.append(new_lot.id)
                        else:
                            # Si ya existe, añade el lote existente a la lista de boxes
                            boxes.append(exist.id)

                    # Asigna los códigos de barras procesados a 'pnt_processed_barcodes'
                    record.pnt_processed_barcodes = [(6, 0, boxes)]

from odoo import api, fields, models

class StockPicking(models.Model):
    _inherit = "stock.picking"

    status=fields.Selection([('2','Stock Updated')], readonly=True, default='2', string='Inventory Status')        


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    status=fields.Selection([('1','Ready To Update'),('2','Stock Updated')], readonly=True, default='1', string='Inventory Status')        


#Update Inventory For Based On Received Quantity in Vendor Bills
    @api.multi
    def update_inventory(self):
        picking_data={
        'name':self.number,
        'origin':self.reference,
        'scheduled_date':self.date_invoice,
        'date':self.date,
        'location_id':8,
        'location_dest_id':12,
        'picking_type_id':1,
        'partner_id':self.partner_id.id,
        'owner_id':self.company_id.id,
        'company_id':self.company_id.id,
        'move_type':'direct',
        'state':'assigned'
        }
        picking_id = self.env['stock.picking'].create(picking_data)

        for product in self.invoice_line_ids:
            move_data = {
            'picking_id':picking_id.id,
            'name': product.name,
            'sequence':10,
            'date':self.date_invoice,
            'company_id':product.company_id.id,
            'product_id':product.product_id.id,
            'ordered_qty':product.quantity,
            #'product_qty':product.quantity,
            'product_uom_qty':product.quantity,
            'product_uom':product.uom_id.id,
            'location_id':8,
            'location_dest_id':12,
            'state': 'confirmed',
            'procure_method':'make_to_stock',
            'scrapped':'f',
            'picking_type_id':1,
            'reference':self.number,
            'date_expected':self.date_invoice
            }
            move_id = self.env['stock.move'].create(move_data)

            move_line={
            'picking_id':picking_id.id,
            'move_id':move_id.id,
            'product_id':product.product_id.id,
            'product_uom_id':product.uom_id.id,
            #'product_qty':product.quantity,
            'product_uom_qty':product.quantity,
            'ordered_qty':product.quantity,
            'qty_done':product.quantity,
            'date':self.date_invoice,
            'owner_id':self.company_id.id,
            'location_id':8,
            'location_dest_id':12,
            'state':'confirmed'
            }
            move_line_id = self.env['stock.move.line'].create(move_line)
        picking_id.action_assign()
        picking_id.button_validate()
        self.status='2'
        return True
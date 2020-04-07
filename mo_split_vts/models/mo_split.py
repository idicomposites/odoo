from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.exceptions import Warning
    
class SplitManufactureOrder(models.TransientModel):
    _name = 'split.mo'
    _description = 'Split Manufacturing Order'
    
    split_mo_lot = fields.Integer(string='Numero de Cant/Split', required=True,help="Split MO Based on Configuration Like Number Of Qty/Lot.based on that split the MO of that Qty and decrease the product qty from Main MO.")
    
    def split_mo(self):
        mo_obj = self.env['mrp.production']
        split_mo_based_on = self.env['ir.config_parameter'].sudo().get_param('mo_split_vts.mo_split_based_on')
        if self._context.get('active_id') and self._context.get('active_model')=='mrp.production':
            mo_id = mo_obj.browse(self.env.context['active_id'])
            if mo_id.state not in ('confirmed'):
                raise UserError(_("You can not split MO in state %s "%(mo_id.state)))
            if split_mo_based_on == 'based_on_number_of_split':
                if not (mo_id.product_qty % self.split_mo_lot == 0):
                    raise Warning('Manufacture Order cannot be split into equal parts.')
                split_qty = mo_id.product_qty/self.split_mo_lot
                for x in range(self.split_mo_lot - 1):
                    copy_mo = mo_id.copy({'main_mo_id':mo_id.id})
                    copy_mo.write({'product_qty':split_qty,'origin':mo_id.name})
                    change_production_qty = self.env['change.production.qty'].create({'mo_id':copy_mo.id,'product_qty':split_qty})
                    change_production_qty.change_prod_qty()
                    copy_mo.action_assign()
            else:
                if self.split_mo_lot <= 0:
                    raise Warning('Qty Must be Grater Than Zero.')
                split_qty = mo_id.product_qty - self.split_mo_lot
                copy_mo = mo_id.copy({'main_mo_id':mo_id.id})
                copy_mo.write({'product_qty':self.split_mo_lot,'origin':mo_id.name})
                change_production_qty = self.env['change.production.qty'].create({'mo_id':copy_mo.id,'product_qty':self.split_mo_lot})
                change_production_qty.change_prod_qty()
                copy_mo.action_assign()
            mo_id.write({'product_qty':split_qty,'main_mo_id':copy_mo.id})
            change_production_qty = self.env['change.production.qty'].create({'mo_id':mo_id.id,'product_qty':split_qty})
            change_production_qty.change_prod_qty()
            return True

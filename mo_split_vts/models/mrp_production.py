from odoo import api, fields, models, _
    
class ManufacturingOrder(models.Model):
    _inherit = 'mrp.production'
    
    main_mo_id = fields.Many2one('mrp.production',string='Source MO')
    
    def open_slip_wizard(self):
        context = dict(self._context or {})
        context['default_split_mo_lot']=self.as_lote_numero 
        context['active_id']=self.id 
        context['active_model']= 'mrp.production'
        return {
            'name': _("Produccion %s") % self.display_name,
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'views': [[self.env.ref('mo_split_vts.split_manufacture_order_form_view').id, 'form']],
            'res_model': 'split.mo',
            'target': 'new',
            'context': context,
        }
       

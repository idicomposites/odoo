from odoo import api, fields, models, _
    
class ManufacturingOrder(models.Model):
    _inherit = 'mrp.production'
    
    main_mo_id = fields.Many2one('mrp.production',string='Source MO')
    

# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_utils, float_compare    
from datetime import datetime, timedelta, date
from odoo.exceptions import UserError
import logging
from odoo.exceptions import Warning, UserError, AccessError
_logger = logging.getLogger(__name__)

class as_mrp_workorder(models.Model):
    _inherit = "mrp.production"
    
    as_machine_id = fields.Many2one(comodel_name='as.machine', string='Maquina')
    as_lote_numero = fields.Integer(string='Cantidad Lote')
    as_lote_peso = fields.Float(string='Peso x Lote')
    as_tanque = fields.Integer(string='Tanque')
    as_lot = fields.Char(string='Nro. Lote')
    
    @api.onchange('as_lote_numero','as_tanque')
    def onchange_as_tanque(self):
        for order in self:
            if order.as_tanque > order.as_lote_numero:
                raise Warning("La cantidad de Tanque no puede ser mayor a la cantidad de lote")
                order.as_tanque = 0

    @api.onchange('as_lote_peso')
    def onchange_as_peso_lote(self):
        for order in self:
            macine= order.as_machine_id.as_numero
            macine_max= order.as_machine_id.as_max
            macine_min= order.as_machine_id.as_min
            if macine:
              if order.as_lote_peso < float(macine_min) or order.as_lote_peso > float(macine_max):
                raise Warning("Cantidad fuera de la capacidad de la maquina")
                order.as_lote_peso = 0.0                
            else:
                raise Warning("Debe seleccionar una maquina")
                order.as_lote_peso = 0.0

class asMRP(models.Model):
    _inherit = 'stock.move'

    as_lotes = fields.Char(string='Lotes')
    

    # def _get_lotes_lines(self):
    #     resultado = ''
    #     for move in self[0]:
    #         for move_line in move.move_line_ids:
    #             for lots in move_line.lot_produced_ids:
    #                 resultado += lots.name +', '
    #     self.as_lotes = resultado




    
# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import time
import datetime
from time import mktime
from dateutil import parser
from datetime import datetime, timedelta, date

import logging
_logger = logging.getLogger(__name__)

class Contenedor(models.Model):
    _name = "as.contenedor"

    name = fields.Char(string='Nombre Contenedor')
    as_peso = fields.Float(string='Peso Contenedor')
    as_lote = fields.Char(string='Lote')
    picking_id = fields.Many2one(comodel_name='stock.picking', string='Picking_id')
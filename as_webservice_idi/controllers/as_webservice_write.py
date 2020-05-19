# -*- coding: utf-8 -*-
from odoo.tools.translate import _
from odoo import http
from odoo import http
from odoo.http import request
import re
# from tabulate import tabulate
# from bs4 import BeautifulSoup
import json
import sys
import yaml
import logging
_logger = logging.getLogger(__name__)

from werkzeug import urls
from werkzeug.wsgi import wrap_file

def as_convert(txt,digits=50,is_number=False):
    if is_number:
        num = re.sub("\D", "", txt)
        if num == '':
            return 0
        return int(num[0:digits])
    else:
        return txt[0:digits]        

class as_webservice(http.Controller):

    # Clientes WRITE
    '''
    {
        "token":"c70bf37cbc0f4d758cc4651b4f999c6c",
        "name":"1111Test",
        "phone":"1111",
        "street":"1111",
        "email":"1111@gmail.com",
        "rfc":"valid_rfc"
    }
    '''
    @http.route(["/tiamericas/clientes/write/"], auth='public', type="json", methods=['POST'],csrf=False)
    def partner(self, partner_id = None, **pdata):
        post = yaml.load(request.httprequest.data)

        el_token = post['token'] or 'sin_token'
        current_user = request.env['res.users'].sudo().search([('as_token', '=', el_token)])
        if not current_user:
            res_json = json.dumps({'error': ('Token Invalido')})
            callback = post.get('callback')
            return '{0}({1})'.format(callback, res_json)  
        if current_user:
            if post:
                partner = int(post.get('id')) if post.get('id') else 0
                current_partner = request.env['res.partner'].sudo().search([('id', '=', partner)])
                res = {}
                partner_data = {
                    "name": as_convert(post.get('name') or ""), #Nombre cliente
                    "phone": as_convert(post.get('phone') or "", is_number=True), #Telefono
                    "street": as_convert(post.get('street') or ""), #Direccion
                    "email": as_convert(post.get('email') or ""), #Email
                    "vat": as_convert(post.get('rfc') or ""), #Email
                }
                if not current_partner:
                    new_id = request.env['res.partner'].sudo().create(partner_data)
                    res['status'] = 'Create Successfully'
                    res['id'] = new_id.id
                    res_json = json.dumps(res)
                elif current_partner:
                    current_partner.update(partner_data)
                    res['status'] = 'Update Successfully'
                    res['id'] = current_partner.id
                    res_json = json.dumps(res)
        callback = post.get('callback')
        return '{0}({1})'.format(callback, res_json)

    # PRODUCTOS WRITE
    # @http.route(['/tiamericas/productos','/tiamericas/productos/<product_id>'], auth="public", type="http")
    # def product(self, product_id = None, **post):
    #     el_token = post.get('token') or 'sin_token'
    #     current_user = request.env['res.users'].sudo().search([('as_token', '=', el_token)])
    #     if not current_user:
    #         res_json = json.dumps({'error': ('Token Invalido')})
    #         callback = post.get('callback')
    #         return '{0}({1})'.format(callback, res_json)  
    #     if current_user:
    #         filtro = '[]'
    #         # product_model = request.env['product.product']
    #         if product_id:
    #             filtro = [('id','=',product_id)]
    #             product_ids = request.env['product.template'].sudo().search(filtro)
    #         else:
    #             product_ids = request.env['product.template'].sudo().search([])   
          
    #         if not product_ids:
    #             res_json = json.dumps({'error': _('Producto no encontrado')})
    #             callback = post.get('callback')
    #             return '{0}({1})'.format(callback, res_json)
    #         else:
    #             rp = {}
    #             json_dict = []

    #             for product in product_ids:  
    #                 rp = {
    #                         'id': product.id,
    #                         'nombre': product.name,
    #                         'tipo_producto': product.type,
    #                         'categoria_producto': self.obj_to_json(product.categ_id),
    #                         'tipo_producto_idi': product.as_tipo_producto_idi,
    #                         'color': product.as_color,
    #                         'referencia_interna': product.default_code,
    #                         'codigo_barras': product.barcode,
    #                         'precio_venta':	product.list_price,
    #                         'costo': product.standard_price,
    #                         'impuestos_cliente': self.obj_to_json(product.taxes_id),
    #                         'unidad_medida': self.obj_to_json(product.uom_id),
    #                         'unidad_medida_compra':	self.obj_to_json(product.uom_po_id),
    #                     }
    #                 json_dict.append(rp)
    #             res = json.dumps(json_dict)
    #             callback = post.get('callback')
    #             return '{0}({1})'.format(callback, res)

    # # BOM WRITE
    # @http.route(['/tiamericas/bom','/tiamericas/bom/<bom_id>'], auth="public", type="http")
    # def bom(self, bom_id = None, **post):
    #     el_token = post.get('token') or 'sin_token'
    #     current_user = request.env['res.users'].sudo().search([('as_token', '=', el_token)])
    #     if not current_user:
    #         res_json = json.dumps({'error': ('Token Invalido')})
    #         callback = post.get('callback')
    #         return '{0}({1})'.format(callback, res_json)  
    #     if current_user:
    #         filtro = '[]'
    #         # product_model = request.env['product.product']
    #         if bom_id:
    #             filtro = [('id','=',bom_id)]
    #             bom_ids = request.env['mrp.bom'].sudo().search(filtro)
    #         else:
    #             bom_ids = request.env['mrp.bom'].sudo().search([])   
          
    #         if not bom_ids:
    #             res_json = json.dumps({'error': _('BOM no encontrado')})
    #             callback = post.get('callback')
    #             return '{0}({1})'.format(callback, res_json)
    #         else:
    #             rp = {}
    #             json_dict = []

    #             for bom in bom_ids:
    #                 # ensamblar lines
    #                 bom_line = request.env['mrp.bom.line']
    #                 bom_lines = bom_line.sudo().search([('bom_id','=',bom.id)])
    #                 bom_line_json_dict = []
    #                 if bom_lines:
    #                     for bom_line in bom_lines:
    #                         bom_line_json_dict.append({
    #                             "id":bom_line.id,
    #                             "product_id":self.obj_to_json(bom_line.product_id),
    #                             "product_qty":bom_line.product_qty,
    #                             "sequence":bom_line.sequence,
    #                         })
    #                 else:
    #                     bom_line_json_dict = {'error': _('Sin lineas')}

    #                 # Ensamblando registro
    #                 rp = {
    #                         'id': bom.id,
    #                         'product_tmpl_id': self.obj_to_json(bom.product_tmpl_id),
    #                         'product_qty': bom.product_qty,
    #                         'code': bom.code,
    #                         'type': bom.type,
    #                         'bom_lines': bom_line_json_dict,
    #                     }
    #                 json_dict.append(rp)
    #             res = json.dumps(json_dict)
    #             callback = post.get('callback')
    #             return '{0}({1})'.format(callback, res)

    # # MRP WRITE
    # @http.route(['/tiamericas/mrp','/tiamericas/mrp/<mrp_id>'], auth="public", type="http")
    # def mrp(self, mrp_id = None, **post):
    #     el_token = post.get('token') or 'sin_token'
    #     current_user = request.env['res.users'].sudo().search([('as_token', '=', el_token)])
    #     if not current_user:
    #         res_json = json.dumps({'error': ('Token Invalido')})
    #         callback = post.get('callback')
    #         return '{0}({1})'.format(callback, res_json)  
    #     if current_user:
    #         filtro = '[]'
    #         # product_model = request.env['product.product']
    #         if mrp_id:
    #             filtro = [('id','=',mrp_id)]
    #             mrp_ids = request.env['mrp.production'].sudo().search(filtro)
    #         else:
    #             mrp_ids = request.env['mrp.production'].sudo().search([])   
          
    #         if not mrp_ids:
    #             res_json = json.dumps({'error': _('MO no encontrado')})
    #             callback = post.get('callback')
    #             return '{0}({1})'.format(callback, res_json)
    #         else:
    #             rp = {}
    #             json_dict = []
    #             fields_mrp_line = ('id','name','product_uom_qty','quantity_done','product_id')
    #             # fields_mrp_line = ('product_id','id')

    #             for mrp in mrp_ids:
    #                 # Ensamblando registro
    #                 rp = {
    #                         'id': mrp.id,
    #                         'name': mrp.name,
    #                         'as_sale': self.obj_to_json(mrp.as_sale),
    #                         'product_id': self.obj_to_json(mrp.product_id),
    #                         'product_qty': mrp.product_qty,
    #                         # 'bom_name': mrp.bom_id.product_tmpl_id.name,
    #                         # 'bom_id': mrp.bom_id.product_tmpl_id.id,
    #                         'bom_id': self.obj_to_json(mrp.bom_id,('product_tmpl_id','id','product_qty','code')),
    #                         'as_lot': self.obj_to_json(mrp.as_lot),
    #                         'version': mrp.bom_id.version,
    #                         'code': mrp.bom_id.code,
    #                         'date_planned_start': str(mrp.date_planned_start),
    #                         'origin': mrp.origin,
    #                         'main_mo_id': self.obj_to_json(mrp.main_mo_id),
    #                         'as_machine_id': self.obj_to_json(mrp.as_machine_id),
    #                         'as_lote_numero': mrp.as_lote_numero,
    #                         'as_lote_peso': mrp.as_lote_peso,
    #                         'as_tanque': mrp.as_tanque,
    #                         'move_raw_ids': self.obj_to_json(mrp.move_raw_ids,fields_mrp_line),
    #                     }
    #                 json_dict.append(rp)
    #             res = json.dumps(json_dict)
    #             callback = post.get('callback')
    #             return '{0}({1})'.format(callback, res)

    # # STOCK WRITE
    # @http.route(['/tiamericas/stock','/tiamericas/stock/<stock_id>'], auth="public", type="http")
    # def stock(self, stock_id = None, **post):
    #     el_token = post.get('token') or 'sin_token'
    #     current_user = request.env['res.users'].sudo().search([('as_token', '=', el_token)])
    #     if not current_user:
    #         res_json = json.dumps({'error': ('Token Invalido')})
    #         callback = post.get('callback')
    #         return '{0}({1})'.format(callback, res_json)  
    #     if current_user:
    #         filtro = '[]'
    #         # product_model = request.env['product.product']
    #         if stock_id:
    #             filtro = [('id','=',stock_id)]
    #             stock_ids = request.env['stock.picking'].sudo().search(filtro)
    #         else:
    #             stock_ids = request.env['stock.picking'].sudo().search([])
          
    #         if not stock_ids:
    #             res_json = json.dumps({'error': _('MO no encontrado')})
    #             callback = post.get('callback')
    #             return '{0}({1})'.format(callback, res_json)
    #         else:
    #             rp = {}
    #             json_dict = []
    #             fields_stock_line = ('id','name','as_peso','as_lote')
    #             # fields_stock_line = ('product_id','id')

    #             for stock in stock_ids:
    #                 # Ensamblando registro
    #                 rp = {
    #                         'id': stock.id,
    #                         'name': stock.name,
    #                         'origin': stock.origin,
    #                         'picking_type_id': self.obj_to_json(stock.picking_type_id),
    #                         'date_done': str(stock.date_done),
    #                         'as_contenedor_id': self.obj_to_json(stock.as_contenedor_id,fields_stock_line),
    #                     }
    #                 json_dict.append(rp)
    #             res = json.dumps(json_dict)
    #             callback = post.get('callback')
    #             return '{0}({1})'.format(callback, res)

    # # TOKEN
    # @http.route('/tiamericas/get_token', type='json',  auth='user')
    # def get_token(self, **post):        
    #     user = request.env['res.users'].sudo().browse(post['local_context']['uid'])
    #     res = user.get_token()
    #     return res

    # # TOKEN GENERATE
    # # http://localhost:10000/tiamericas/token/?login=admin&password=123&db=ODOO12_APP
    # @http.route(['/tiamericas/token',], auth="public", type="http", csrf=False)
    # def token(self, **post):
    #     """
    #         Para autenticar se deben enviar usuario y password
    #         servidor.com:8069/tiamericas/token?login=admin&password=admin
    #     """
    #     res = {}
    #     try:
    #         uid = request.session.authenticate(request.params['db'], request.params['login'], request.params['password'])
    #         if uid:
    #             user = request.env['res.users'].sudo().browse(uid)
    #             token = user.get_user_access_token()
    #             user.as_token = token
    #             res['token'] = token
    #             request.session.logout()
    #         else:
    #             res['error'] = "Login o Password erroneo"
    #         res_json = json.dumps(res)
    #         callback = post.get('callback')
    #         return '{0}({1})'.format(callback, res_json)
    #     except:
    #         res['error'] = "Envia login y password"
    #         res_json = json.dumps(res)
    #         callback = post.get('callback')
    #         return '{0}({1})'.format(callback, res_json)

    # Convertir objeto a json
    # Fields debe tener al menos 2 valores
    def obj_to_json(self, objeto, fields = None):
        json_dict = []
        rp = {}
        rp2 = []
        if fields:
            if objeto:
                for child in objeto:
                    rp = {}
                    for field in fields:
                        if isinstance(getattr(child, field), (float, int, str)):
                            rp[field] = getattr(child, field)
                        else:
                            rp[field] = self.obj_to_json(getattr(child, field))
                    rp2.append(rp)
                json_dict.append(rp2)
            else:
                json_dict = {'error': _('Not found')}               
        else:
            if objeto:
                for child in objeto:
                    json_dict.append({
                        "id": child.id,
                        "name": child.name, #Nombre cliente
                    })
            else:
                json_dict = {'error': _('Not found')}
        return json_dict


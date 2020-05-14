# # -*- coding: utf-8 -*-

import datetime
from datetime import datetime
import pytz
from odoo import models,fields
from datetime import datetime, timedelta
from time import mktime
from odoo import api, models, _
from odoo.exceptions import UserError
from io import BytesIO
from urllib.request import urlopen
from odoo.tools.image import image_data_uri

class as_kardex_productos_excel(models.AbstractModel):
    _name = 'report.as_idi_mrp.report_certificate_idi.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):        
        dict_almacen = []
        dict_aux = []
        filtro = ''
        # if data['form']['stage_id']:
        #     filtro+= ' and hs.id in '+ str(data['form']['stage_id']).replace('[','(').replace(']',')')
        # if data['form']['partner_id']:
        #     filtro+= ' and rp.id in '+ str(data['form']['partner_id']).replace('[','(').replace(']',')')
        # if data['form']['as_empresa']:
        #     filtro+= ' and ae.id in '+ str(data['form']['as_empresa']).replace('[','(').replace(']',')')
        sheet = workbook.add_worksheet('Detalle de Movimientos')
        sheet.set_paper(1)
        sheet.set_landscape()
        
        titulo1 = workbook.add_format({'font_size': 16, 'align': 'center', 'text_wrap': True, 'bold':True })
        titulo2 = workbook.add_format({'font_size': 14, 'align': 'center', 'text_wrap': True, 'bottom': True, 'top': True, 'bold':True })
        titulo3 = workbook.add_format({'font_size': 12, 'align': 'left', 'text_wrap': True, 'bottom': True, 'top': True })
        titulo3_number = workbook.add_format({'font_size': 14, 'align': 'right', 'text_wrap': True, 'bottom': True, 'top': True, 'bold':True, 'num_format': '#,##0.00' })
        titulo4 = workbook.add_format({'font_size': 12, 'align': 'center', 'text_wrap': True, 'bottom': True, 'top': True, 'left': True, 'right': True})

        number_left = workbook.add_format({'font_size': 12, 'align': 'left', 'num_format': '#,##0.00'})
        number_right = workbook.add_format({'font_size': 12, 'align': 'right', 'num_format': '#,##0.00'})
        number_right_bold = workbook.add_format({'font_size': 12, 'align': 'right', 'num_format': '#,##0.00', 'bold':True})
        number_right_col = workbook.add_format({'font_size': 12, 'align': 'right', 'num_format': '#,##0.00','bg_color': 'silver'})
        number_center = workbook.add_format({'font_size': 12, 'align': 'center', 'num_format': '#,##0.00'})
        number_right_col.set_locked(False)

        letter12 = workbook.add_format({'font_size': 12, 'align': 'center', 'text_wrap': True, 'bold':True,'bottom': True, 'top': True, 'left': True, 'right': True})
        letter11 = workbook.add_format({'font_size': 12, 'align': 'center', 'text_wrap': True,'bottom': True, 'top': True, 'left': True, 'right': True})
        letter1 = workbook.add_format({'font_size': 12, 'align': 'left', 'text_wrap': True})
        letter1d = workbook.add_format({'font_size': 10, 'align': 'center', 'text_wrap': True})
        letter2 = workbook.add_format({'font_size': 12, 'align': 'left', 'bold':False})
        letter3 = workbook.add_format({'font_size': 12, 'align': 'right', 'text_wrap': True})
        letter4 = workbook.add_format({'font_size': 12, 'align': 'left', 'text_wrap': True, 'bold': True})
        letter5 = workbook.add_format({'font_size': 12, 'align': 'right', 'text_wrap': True, 'bold': True})
        letter_locked = letter3
        letter_locked.set_locked(False)

        # Aqui definimos en los anchos de columna
        sheet.set_column('A:A',4, letter1)
        sheet.set_column('B:B',15, letter1)
        sheet.set_column('C:C',15, letter1)
        sheet.set_column('D:D',10, letter1)
        sheet.set_column('E:E',10, letter1)
        sheet.set_column('F:F',10, letter1)
        sheet.set_column('G:G',10, letter1)
        sheet.set_column('H:H',10, letter1)
        sheet.set_column('I:I',10, letter1)
        sheet.set_column('J:J',10, letter1)
        sheet.set_column('K:K',10, letter1)
        sheet.merge_range(3,4,4,7,'BMC Certificate Of Analysis',titulo1) 
        # fecha_inicial = datetime.strptime(data['form']['start_date'], '%Y-%m-%d').strftime('%d/%m/%Y')
        # fecha_final = datetime.strptime(data['form']['end_date'], '%Y-%m-%d').strftime('%d/%m/%Y')
        # # Titulos, subtitulos, filtros y campos del reporte.
        url = image_data_uri(self.env.user.company_id.logo)
        image_data = BytesIO(urlopen(url).read())
        sheet.insert_image('B1', url, {'image_data': image_data})      
        fecha = (datetime.now() - timedelta(hours=4)).strftime('%d/%m/%Y %H:%M:%S')
        customer = ''
        mrp = self.env['mrp.production'].search([('as_lot', '=', lines.lot_id.id)])
        if mrp:
            customer=mrp.as_sale.partner_id.name
        sheet.write(3, 1, 'Material: ',letter1) 
        sheet.write(3, 2, lines.product_id.default_code,letter2)         
        sheet.write(4, 1, 'Color: ',letter1) 
        sheet.write(4, 2, lines.product_id.as_color,letter2) 
        sheet.write(5, 1, 'Customer: ',letter1) 
        sheet.write(5, 2, customer,letter2)         
        sheet.write(6, 1, 'Commercial Guarantee: ',letter1) 
        sheet.write(6, 2, '',letter2) 

        # sheet.merge_range('A2:D2', 'Dirección: '+self.env.user.company_id.street, letter1)
        # sheet.merge_range('A3:D3', 'Telefono: '+self.env.user.company_id.phone, letter1)
        # sheet.merge_range('A4:D4', str(self.env.user.company_id.city)+'-'+str(self.env.user.company_id.country_id.name))
        # sheet.merge_range('F1:I1', 'Usuario Impresión: '+self.env.user.name, letter1)
        # sheet.merge_range('F2:I2', 'Fecha y Hora Impresión: '+fecha, letter1)
         
        #sheet.merge_range('A5:I5', 'REPORTE DE TICKETS SOPORTE', titulo1)
        #sheet.set_row(7, 40)
        #sheet.merge_range('A6:I6', 'DEL '+fecha_inicial+' AL '+fecha_final, letter11)
        filas = 7
        filas += 1
        code_format = lines.product_id.as_format_type_id.as_code
        point_array =[]
        point_all = self.env['quality.point'].search([('product_tmpl_id', '=', lines.product_id.product_tmpl_id.id)])
        quality_check_all = self.env['quality.check'].search([('lot_id', '=', lines.lot_id.id)])
        for quelity in quality_check_all:
            for point in point_all:
                if quelity.point_id.id == point.id:
                    point_array.append(point.id)
        point = self.env['quality.point'].search([('id', 'in', point_array)])
        quality_check = self.env['quality.check'].search([('product_id', '=', lines.product_id.id)])
        if code_format == 4:
            filas += 1
            sheet.merge_range('B7:E7', 'Propierty', letter12)
            sheet.merge_range('F7:H7', 'Unit', letter12)
            sheet.merge_range('I7:K7', 'Specification', letter12)
            sheet.merge_range('L7:M7', 'Reference Method', letter12)
            filas += 1
            cont=7
            for item in point_all:
                cont +=1
                sheet.merge_range('B'+str(cont)+':E'+str(cont), item.title, letter11)
                sheet.merge_range('F'+str(cont)+':H'+str(cont), item.norm_unit, letter11)
                sheet.merge_range('I'+str(cont)+':K'+str(cont), str(item.tolerance_min)+'-'+str(item.tolerance_max), letter11)
                sheet.merge_range('L'+str(cont)+':M'+str(cont), item.operation_id.name, letter11)
                filas += 1
        if int(code_format) >= 3:
            sheet.write(filas, 1, 'Batch',letter12) #cliente/proveedor
            sheet.write(filas, 2, 'Manufacturing Date',letter12) #cliente/proveedor
            sheet.write(filas, 3, '# Box',letter12) #cliente/proveedor
            cont =4
            for intem in point:
                sheet.write(filas, cont, intem.title+'('+intem.norm_unit+')',letter12) #cliente/proveedor   
                cont+=1
            filas += 1
            quality_check = self.env['quality.check'].search([('lot_id', '=', lines.lot_id.id)])
            dia = datetime.strptime(str(lines.control_date), '%Y-%m-%d %H:%M:%S.%f').strftime('%d')
            mes = datetime.strptime(str(lines.control_date), '%Y-%m-%d %H:%M:%S.%f').strftime('%m')
            year = datetime.strptime(str(lines.control_date), '%Y-%m-%d %H:%M:%S.%f').strftime('%Y')
            fecha = str(dia)+'/'+str(self.get_mes(mes))+'/'+year
            sheet.write(filas, 1,lines.lot_id.name,letter11) 
            sheet.write(filas, 2,fecha,letter11) 
            caja=''
            if 'x_studio__box' in lines:
                caja = lines.x_studio__box
            sheet.write(filas, 3,caja,letter11) 
            cont =4
            for intem in point:
                value = 0.0
                for item in quality_check:
                    if intem.id == item.point_id.id:
                        value = item.measure
                sheet.write(filas, cont, float(value),letter11) #cliente/proveedor   
                cont+=1
            filas += 1
        else:
            sheet.merge_range(filas,1,filas+2,1,'Batch',letter11)
            sheet.merge_range(filas,2,filas+2,2,'Manufacturing Date',letter11)
            # sheet.merge_range(8,3,8,5,'hola1',letter12) #cliente/proveedor   
            # sheet.merge_range(8,6,8,8,'hola2',letter12) #cliente/proveedor   
            # sheet.merge_range(9,3,9,5,'hola3',letter12) #cliente/proveedor   

            cont =3
            for intem in point:
                sheet.merge_range(filas,cont,filas,cont+2,str(intem.title)+'('+str(intem.norm_unit)+')',letter11)
                sheet.merge_range(filas+1,cont,filas+1,cont+1,'Specification',letter11)
                sheet.merge_range(filas+1,cont+2,filas+2,cont+2,'Result',letter11)
                sheet.write(filas+2, cont, 'Max',letter11) #cliente/proveedor
                sheet.write(filas+2, cont+1, 'Min',letter11) #cliente/proveedor
                cont+=3
            filas += 3
            quality_check = self.env['quality.check'].search([('lot_id', '=', lines.lot_id.id)])
            dia = datetime.strptime(str(lines.control_date), '%Y-%m-%d %H:%M:%S.%f').strftime('%d')
            mes = datetime.strptime(str(lines.control_date), '%Y-%m-%d %H:%M:%S.%f').strftime('%m')
            year = datetime.strptime(str(lines.control_date), '%Y-%m-%d %H:%M:%S.%f').strftime('%Y')
            fecha = str(dia)+'/'+str(self.get_mes(mes))+'/'+year
            sheet.write(filas, 1,lines.lot_id.name,letter11) 
            sheet.write(filas, 2,fecha,letter11) 
            cont =3
            for intem in point:
                value = 0.0
                for item in quality_check:
                    if intem.id == item.point_id.id:
                        value = item.measure
                sheet.write(filas, cont, str(intem.tolerance_min),letter11) #cliente/proveedor   
                cont+=1                
                sheet.write(filas, cont, str(intem.tolerance_max),letter11) #cliente/proveedor   
                cont+=1                
                sheet.write(filas, cont, float(value),letter11) #cliente/proveedor   
                cont+=1
            filas += 1
        filas += 2
        sheet.merge_range(filas,1,filas+6,11,lines.product_id.as_format_type_id.as_slogan,letter1) #cliente/proveedor 
        filas += 8
        sheet.merge_range(filas,4,filas+5,6,lines.product_id.as_format_type_id.as_sfooter,letter1d) 
        url = image_data_uri(lines.product_id.as_format_type_id.image)
        image_data = BytesIO(urlopen(url).read())
        sheet.insert_image('J'+str(filas+2), url, {'image_data': image_data}) 
        sheet.merge_range(filas+4,9,filas+4,10,lines.product_id.as_format_type_id.as_code_iso,letter1) 


    def get_mes(self,mes):
        mesesDic = {
            "01":'Ene',
            "02":'Feb',
            "03":'Mar',
            "04":'Abr',
            "05":'May',
            "06":'Jun',
            "07":'Jul',
            "08":'Ago',
            "09":'Sep',
            "10":'Oct',
            "11":'Nov',
            "12":'Dic',
        }
        return mesesDic[str(mes)]
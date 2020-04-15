# -*- coding: utf-8 -*-
{
    'name' : "Ahorasoft MRP customizaciones",
    'version' : "1.0.2",
    'author'  : "Ahorasoft",
    'description': """
Customizaciones para VAXMEX
===========================

Custom module for Latproject
    """,
    'category' : "MRP",
    'depends' : ["mrp","product",'sale','purchase','stock'],
    'website': 'http://www.ahorasoft.com',
    'data' : [
        'security/ir.model.access.csv',
        'views/as_mrp_production.xml',
        'views/as_machine.xml',
        'views/as_product_category.xml',
        'wizard/mrp_product_produce.xml',
        'views/as_sale_order.xml',
        'views/as_stock_picking.xml',
        'views/as_contenedor.xml'
             ],
    'demo' : [],
    'installable': True,
    'auto_install': False
}

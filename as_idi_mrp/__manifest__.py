# -*- coding: utf-8 -*-
{
    'name' : "Ahorasoft MRP customizaciones",
    'version' : "1.0.0",
    'author'  : "Ahorasoft",
    'description': """
Customizaciones para VAXMEX
===========================

Custom module for Latproject
    """,
    'category' : "MRP",
    'depends' : ["mrp","product",'sale','purchase'],
    'website': 'http://www.ahorasoft.com',
    'data' : [
        'security/ir.model.access.csv',
        'views/as_mrp_production.xml',
        'views/as_machine.xml',
        'views/as_product_category.xml',
        'wizard/mrp_product_produce.xml',
        'views/as_sale_order.xml'
             ],
    'demo' : [],
    'installable': True,
    'auto_install': False
}

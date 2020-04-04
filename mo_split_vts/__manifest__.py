{
    'name': 'Split Manufacturing Order ',
    'version': '13.0.16.10.2019',
    'category': 'Manufacturing',
    'author': "Vraja Technologies",
    'price': 27
,
    'currency': 'EUR',
    'summary':"This Module Allow us to Split Manufacturing Order Based on Number of Split.Split Mo in Equal Part",
    'depends': [
        'mrp',
    ],
    'data': [
        'views/mo_split_view.xml',
        'views/mrp_production.xml',
        'wizard/res_config.xml',
    ],
    'qweb': [],
    'css': [],
    'js': [],
    'images': [
        'static/description/split_mo_wizard.png',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'OPL-1',
}

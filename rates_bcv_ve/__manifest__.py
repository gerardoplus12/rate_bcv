# -*- coding: utf-8 -*-
{
    'name': 'Tasas de Cambio BCV',
    'version': '19.0.1.0.0',
    'summary': 'Obtiene tasas de USD y EUR directamente del BCV vía Scraping',
    'description': 'Obtiene tasas de USD y EUR directamente del BCV vía Scraping',
    'category': 'Accounting',
    'author': 'Rodriguez G.',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/rates_daily_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

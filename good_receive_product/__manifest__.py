# -*- coding: utf-8 -*-
{
    'name': 'Good Receive Product',

    'version': '12.0.1',

    'summary': 'Increased fields in picking form',

    'description': """
       * Added unit price, subtotal and total field in picking form 
    """,

    'category': 'Stock',

    'website': "www.asiamatrixsoftware.com",

    'email': 'info@asiamatrixsoftware.com',

    'depends': [
        'stock',
        'purchase_stock',
    ],

    'data': [
       'views/stock_picking_income_views.xml',
    ],

    'installable': True,

    'application': False,

    'auto_install': False,
}

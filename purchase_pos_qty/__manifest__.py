# -*- coding: utf-8 -*-
{
    'name': 'Purchase By POS Qty',

    'version': '12.0.1.0',

    'summary': 'AddedPOS total quantity field in purchase order line',

    'description': """
       * Added last month product total POS quantity field in purchase order line.
    """,

    'category': 'Purchase',

    'website': "www.asiamatrixsoftware.com",

    'email': 'info@asiamatrixsoftware.com',

    'depends': [
        'purchase',
        'point_of_sale',
    ],

    'data': [
        'views/purchase_views.xml',
    ],

    'installable': True,

    'application': False,

    'auto_install': False,
}

# -*- coding: utf-8 -*-
{
    'name': "Purchase Percentage",

    'summary': "Added Sale price and Markup Percentage",

    'description': """
        Added Sale price and Markup Percentage column in Purchase Order Line.
    """,

    'category': 'Contact',

    'version': '0.1',

    'depends': [
        'purchase',
    ],

    'data': [
        'views/purchase_views.xml',
    ],

    'application': True,

    'installable': True,
}

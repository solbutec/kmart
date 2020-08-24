
{
    'name': "inventory_extension",
    'summary': """Edit field on Stock Modules""",
    'description': """To add Stock Location with Internal filter in Inventory adjustment """,
    'author': "Tin Htoo Aug",
    'website': "asiamatrixsoftware.com",
    'category': 'inventory_extension',
    'version': '12.0.0.1',
    'depends': ['stock'],
    'data': [
        'views/inventory_extension_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'application': False,
    'installable': True,
    'auto_install': False,
}
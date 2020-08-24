{
    'name': 'POS Multi UOM',
    'sequence': 10,
    'version': '12.2.0',
    'description': 'Unit of Measure, Units, Measure, Pos, Multi, UOM',
    'summary': 'Allow sell a product with multi units of measure on POS.',
    'category': 'Point of Sale',
    'depends': ['point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/header.xml',
        'views/config.xml',
        'views/pos_order.xml'
    ],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'application': True,
    'price': 80,
    'license': 'OPL-1',
    'currency': 'EUR',
    'author': 'Matrix',
    'images': ['static/description/banner.png'],

}

{
    'name': 'Product Multi Barcode for POS',
    'author': '',
    'version': '12.0.1.5', 
    'summary': 'Product Multi Barcode for POS',
    'description': """
        Product Multi Barcode for POS
    """,
    'depends': ['base','point_of_sale'],
    'data': [
            'security/ir.model.access.csv',
            'views/product_template_view.xml',],
    'installable': True,
    'auto_install': False,
    'application': True,
    'category': 'Point of Sale',
    
}

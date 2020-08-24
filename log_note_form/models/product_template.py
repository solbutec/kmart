import itertools

from odoo.addons import decimal_precision as dp

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, RedirectWarning, UserError
from odoo.osv import expression
from odoo.tools import pycompat


class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = ['product.template','mail.thread', 'mail.activity.mixin']
    _description = "Product Template"
    _order = "name"

    def _get_default_category_id(self):
        if self._context.get('categ_id') or self._context.get('default_categ_id'):
            return self._context.get('categ_id') or self._context.get('default_categ_id')
        category = self.env.ref('product.product_category_all', raise_if_not_found=False)
        if not category:
            category = self.env['product.category'].search([], limit=1)
        if category:
            return category.id
        else:
            err_msg = _('You must define at least one product category in order to be able to create products.')
            redir_msg = _('Go to Internal Categories')
            raise RedirectWarning(err_msg, self.env.ref('product.product_category_action_form').id, redir_msg)

    def _get_default_uom_id(self):
        return self.env["uom.uom"].search([], limit=1, order='id').id

    name = fields.Char('Name', index=True, required=True, translate=True,track_visibility="always")
    sequence = fields.Integer('Sequence', default=1, help='Gives the sequence order when displaying a product list')
    description = fields.Text(
        'Description', translate=True)
    description_purchase = fields.Text(
        'Purchase Description', translate=True)
    description_sale = fields.Text(
        'Sale Description', translate=True,
        help="A description of the Product that you want to communicate to your customers. "
             "This description will be copied to every Sales Order, Delivery Order and Customer Invoice/Credit Note")
    # type = fields.Selection([
    #     ('consu', 'Consumable'),
    #     ('service', 'Service')], string='Product Type', default='consu', required=True,
    #     help='A storable product is a product for which you manage stock. The Inventory app has to be installed.\n'
    #          'A consumable product is a product for which stock is not managed.\n'
    #          'A service is a non-material product you provide.',track_visibility='always')
    type = fields.Selection(selection_add=[('product', 'Storable Product')],track_visibility='always')
    rental = fields.Boolean('Can be Rent')
    categ_id = fields.Many2one(
        'product.category', 'Product Category',
        change_default=True, default=_get_default_category_id,
        required=True, help="Select category for the current product",track_visibility="always")
    uom_category = fields.Many2one('uom.category',string="UOM Categories",required=True,track_visibility='always')

    product_cut=fields.Many2one('product.item',string="Product Cut Items",)



    currency_id = fields.Many2one(
        'res.currency', 'Currency', compute='_compute_currency_id')
    cost_currency_id = fields.Many2one(
        'res.currency', 'Cost Currency', compute='_compute_cost_currency_id')

    # price fields
    # price: total template price, context dependent (partner, pricelist, quantity)
    price = fields.Float(
        'Price', compute='_compute_template_price', inverse='_set_template_price',
        digits=dp.get_precision('Product Price'),track_visibility='always')
    # list_price: catalog price, user defined
    list_price = fields.Float(
        'Sales Price', default=1.0,
        digits=dp.get_precision('Product Price'),
        help="Price at which the product is sold to customers.",trick_visibility="always")
    # lst_price: catalog price for template, but including extra for variants
    lst_price = fields.Float(
        'Public Price', related='list_price', readonly=False,
        digits=dp.get_precision('Product Price'),track_visibility='always')
    standard_price = fields.Float(
        'Cost', compute='_compute_standard_price',
        inverse='_set_standard_price', search='_search_standard_price',
        digits=dp.get_precision('Product Price'), groups="base.group_user",
        help = "Cost used for stock valuation in standard price and as a first price to set in average/FIFO.",track_visibility='always')

    volume = fields.Float(
        'Volume', compute='_compute_volume', inverse='_set_volume',
        help="The volume in m3.", store=True)
    weight = fields.Float(
        'Weight', compute='_compute_weight', digits=dp.get_precision('Stock Weight'),
        inverse='_set_weight', store=True,
        help="The weight of the contents in Kg, not including any packaging, etc.")
    weight_uom_id = fields.Many2one('uom.uom', string='Weight Unit of Measure', compute='_compute_weight_uom_id')
    weight_uom_name = fields.Char(string='Weight unit of measure label', related='weight_uom_id.name', readonly=True)

    sale_ok = fields.Boolean('Can be Sold', default=True)
    purchase_ok = fields.Boolean('Can be Purchased', default=True)
    pricelist_id = fields.Many2one(
        'product.pricelist', 'Pricelist', store=False,
        help='Technical field. Used for searching on pricelists, not stored in database.')
    uom_id = fields.Many2one(
        'uom.uom', 'Unit of Measure',
        default=_get_default_uom_id, required=True,
        help="Default unit of measure used for all stock operations.",track_visibility="always")
    uom_name = fields.Char(string='Unit of Measure Name', related='uom_id.name', readonly=True,track_visibility="always")
    uom_po_id = fields.Many2one(
        'uom.uom', 'Purchase Unit of Measure',
        default=_get_default_uom_id, required=True,
        help="Default unit of measure used for purchase orders. It must be in the same category as the default unit of measure.",track_visibility="always")
    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env['res.company']._company_default_get('product.template'), index=1)
    packaging_ids = fields.One2many(
        'product.packaging', string="Product Packages", compute="_compute_packaging_ids", inverse="_set_packaging_ids",
        help="Gives the different ways to package the same product.")
    seller_ids = fields.One2many('product.supplierinfo', 'product_tmpl_id', 'Vendors', help="Define vendor pricelists.")
    variant_seller_ids = fields.One2many('product.supplierinfo', 'product_tmpl_id')

    active = fields.Boolean('Active', default=True, help="If unchecked, it will allow you to hide the product without removing it.")
    color = fields.Integer('Color Index')

    is_product_variant = fields.Boolean(string='Is a product variant', compute='_compute_is_product_variant')
    attribute_line_ids = fields.One2many('product.template.attribute.line', 'product_tmpl_id', 'Product Attributes')

    valid_product_template_attribute_line_ids = fields.Many2many('product.template.attribute.line',
        compute="_compute_valid_attributes", string='Valid Product Attribute Lines', help="Technical compute")
    valid_product_attribute_value_ids = fields.Many2many('product.attribute.value',
        compute="_compute_valid_attributes", string='Valid Product Attribute Values', help="Technical compute")
    valid_product_attribute_ids = fields.Many2many('product.attribute',
        compute="_compute_valid_attributes", string='Valid Product Attributes', help="Technical compute")
    # wnva = without no_variant attributes
    valid_product_template_attribute_line_wnva_ids = fields.Many2many('product.template.attribute.line',
        compute="_compute_valid_attributes", string='Valid Product Attribute Lines Without No Variant Attributes', help="Technical compute")
    valid_product_attribute_value_wnva_ids = fields.Many2many('product.attribute.value',
        compute="_compute_valid_attributes", string='Valid Product Attribute Values Without No Variant Attributes', help="Technical compute")
    valid_product_attribute_wnva_ids = fields.Many2many('product.attribute',
        compute="_compute_valid_attributes", string='Valid Product Attributes Without No Variant Attributes', help="Technical compute")
    valid_archived_variant_ids = fields.Many2many('product.product',
        compute="_compute_valid_attributes", string='Valid Archived Variants', help="Technical compute")
    valid_existing_variant_ids = fields.Many2many('product.product',
        compute="_compute_valid_existing_variant_ids", string='Valid Existing Variants', help="Technical compute")

    product_variant_ids = fields.One2many('product.product', 'product_tmpl_id', 'Products', required=True)
    # performance: product_variant_id provides prefetching on the first product variant only
    product_variant_id = fields.Many2one('product.product', 'Product', compute='_compute_product_variant_id')

    product_variant_count = fields.Integer(
        '# Product Variants', compute='_compute_product_variant_count')

    # related to display product product information if is_product_variant
    barcode = fields.Char('Barcode', oldname='ean13', related='product_variant_ids.barcode', readonly=False,track_visibility="always")
    default_code = fields.Char(
        'Internal Reference', compute='_compute_default_code',
        inverse='_set_default_code', store=True)

    item_ids = fields.One2many('product.pricelist.item', 'product_tmpl_id', 'Pricelist Items')

    # image: all image fields are base64 encoded and PIL-supported
    image = fields.Binary(
        "Image", attachment=True,
        help="This field holds the image used as image for the product, limited to 1024x1024px.")
    image_medium = fields.Binary(
        "Medium-sized image", attachment=True,
        help="Medium-sized image of the product. It is automatically "
             "resized as a 128x128px image, with aspect ratio preserved, "
             "only when the image exceeds one of those sizes. Use this field in form views or some kanban views.")
    image_small = fields.Binary(
        "Small-sized image", attachment=True,
        help="Small-sized image of the product. It is automatically "
             "resized as a 64x64px image, with aspect ratio preserved. "
             "Use this field anywhere a small image is required.")



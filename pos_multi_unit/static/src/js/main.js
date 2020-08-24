odoo.define('pos_multi_uom.main', function (require) {
    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var PopupWidget = require('point_of_sale.popups');
    var gui = require('point_of_sale.gui');
    var core = require('web.core');
    var qweb = core.qweb;

    models.load_models([
        {
            model: 'product.multi.uom',
            fields: [],
            domain: null,
            loaded: function (self, uoms) {
                self.uom_by_id = {};
                self.uoms_by_product_tmpl_id = {};

                uoms.forEach(function (item) {
                    self.uom_by_id[item.id] = item;

                    if (!self.uoms_by_product_tmpl_id[item.product_tmpl_id[0]]) {
                        self.uoms_by_product_tmpl_id[item.product_tmpl_id[0]] = [item];
                    } else {
                        self.uoms_by_product_tmpl_id[item.product_tmpl_id[0]].push(item)
                    }
                })
            }
        }
    ]);

    var _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        initialize: function (attr, options) {
            _super_orderline.initialize.call(this, attr, options);
            this.uom_id = this.get_product().uom_id[0] || false;

        },
        init_from_JSON: function (json) {
            _super_orderline.init_from_JSON.apply(this, arguments);
            this.uom_id = json.uom_id || false;
        },
        export_as_JSON: function () {
            var json = _super_orderline.export_as_JSON.apply(this, arguments);
            json.uom_id = this.uom_id || false;
            return json;
        },
        get_unit: function () {
            if (this.uom_id){
                var unit = this.pos.units_by_id[this.uom_id];
                return unit;
            }
        },
        set_uom: function (uom) {
            if (!uom){
                return;
            }

            var product = this.get_product();
            var o_lst_price = product.lst_price;
            var o_uom_id = product.uom_id;

            // assign new
            product.lst_price = uom.price;
            product.uom_id = uom.uom_id;

            var price = product.get_price(this.order.pricelist, this.get_quantity());

            this.uom_id = uom.uom_id[0];

            this.set_unit_price(price);
            this.trigger('change', this);

            // back to default
            product.lst_price = o_lst_price;
            product.uom_id = o_uom_id;
        },
        set_quantity: function (quantity, keep_price){
            _super_orderline.set_quantity.call(this, quantity, keep_price);
            var _id = this.uom_id;
            var uoms = this.pos.uoms_by_product_tmpl_id[this.get_product().product_tmpl_id];

            if (!uoms) {
                return;
            }

            var _uom;
            uoms.forEach(function (uom) {
                if (uom.uom_id[0] === _id) {
                    _uom = uom;
                }
            });

            if (_uom) {
                this.set_uom(_uom);
            }
        },
    });

    var options_popup = PopupWidget.extend({
        template: 'OptionsPopup',
        renderElement: function () {
            var self = this;
            this._super();

            var uoms = this.options.uoms || false;
            if (!uoms) {
                return;
            }

            uoms.forEach(function (uom) {
                var uom_line = $(qweb.render('UomLine', {
                    widget: self,
                    uom: uom
                }));
                self.$('.uom-list-content').append(uom_line);
            });

            this.$('.uom-line').on('click', function (){

                var id = parseInt($(this).attr('id'));

                var uom = false;
                if (id === -1){
                    uom = uoms[0];
                }else{
                    uom = self.pos.uom_by_id[id];
                }

                self.options.selected_line.set_uom(uom);
                self.gui.close_popup();
            });
        }
    });
    gui.define_popup({
        name: 'options_popup',
        widget: options_popup
    });


    var options_btn = screens.ActionButtonWidget.extend({
        template: 'OptionsBtn',
        button_click: function () {
            var self = this;
            var order = this.pos.get_order();

            if (!order) {
                return;
            }

            var selected_orderline = order.selected_orderline;

            if (!selected_orderline) {
                return;
            }

            var product = selected_orderline.product;

            var default_uom = {
                uom_id: product.uom_id,
                price: product.lst_price,
                ratio: 1,
                base_uom_id: product.uom_id
            };
            var uoms_by_product = this.pos.uoms_by_product_tmpl_id[product.product_tmpl_id];
            var uoms = [default_uom].concat(uoms_by_product);
            if (uoms_by_product && uoms.length >= 2) {
                self.gui.show_popup('options_popup', {uoms: uoms, selected_line: selected_orderline});
            }
        }
    });
    screens.define_action_button({
        'name': 'options_btn',
        'widget': options_btn,
        'condition': function () {
            return true;
        }
    });

    screens.ClientListScreenWidget.include({
    	save_changes: function(){
            var order = this.pos.get_order();
            if( this.has_client_changed() ){
                var default_fiscal_position_id = _.findWhere(this.pos.fiscal_positions, {'id': this.pos.config.default_fiscal_position_id[0]});
                if ( this.new_client ) {
                    if (this.new_client.property_account_position_id ){
                      var client_fiscal_position_id = _.findWhere(this.pos.fiscal_positions, {'id': this.new_client.property_account_position_id[0]});
                      order.fiscal_position = client_fiscal_position_id || default_fiscal_position_id;
                    }
//                    order.set_pricelist(_.findWhere(this.pos.pricelists, {'id': this.new_client.property_product_pricelist[0]}) || this.pos.default_pricelist);
                } else {
                    order.fiscal_position = default_fiscal_position_id;
//                    order.set_pricelist(this.pos.default_pricelist);
                }

                order.set_client(this.new_client);
            }
        },
    })
    
});
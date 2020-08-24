odoo.define('mai_multibarcode_options_pos.pos', function(require) {
	"use strict";

	var models = require('point_of_sale.models');
	var screens = require('point_of_sale.screens');
	var core = require('web.core');
	var gui = require('point_of_sale.gui');
	var popups = require('point_of_sale.popups');
	var QWeb = core.qweb;
	var PosDB = require('point_of_sale.DB');
	var rpc = require('web.rpc');
	var _t = core._t;

	var _super_posmodel = models.PosModel.prototype;
	models.PosModel = models.PosModel.extend({
		initialize: function (session, attributes) {
			var product_model = _.find(this.models, function(model){ return model.model === 'product.product'; });
			return _super_posmodel.initialize.call(this, session, attributes);

		},

		scan_product: function(parsed_code){
			var selectedOrder = this.get_order();
			var self = this;
			var product = this.db.get_product_by_barcode(parsed_code.base_code);
			rpc.query({
				model: 'product.product',
				method: 'get_multi_barcode_product',
				args: [1,parsed_code.code],
			}, {async: false}).then(function(output) {
				if(output)
				{
					product = self.db.get_product_by_id(output);
				}
			});
			if(!product){
				return false;
			}

			if(parsed_code.type === 'price'){
				selectedOrder.add_product(product, {price:parsed_code.value});
			}else if(parsed_code.type === 'weight'){
				selectedOrder.add_product(product, {quantity:parsed_code.value, merge:false});
			}else if(parsed_code.type === 'discount'){
				selectedOrder.add_product(product, {discount:parsed_code.value, merge:false});
			}else{
				selectedOrder.add_product(product);
			}
			return true;
		},
	});

	screens.ProductCategoriesWidget.include({
		perform_search: function(category, query, buy_result){
			var self = this;
			var products;
			if(query){
				products = this.pos.db.search_product_in_category(category.id,query);
				rpc.query({
					model: 'product.product',
					method: 'get_multi_barcode_search',
					args: [1,query],
				}, {async: false}).then(function(output) {
					if(output)
					{
						for (var i = 0; i < output.length; i++) {
							
							products.push(self.pos.db.get_product_by_id(output[i]))
						}
					}
					if(buy_result && products.length === 1){
	                    self.pos.get_order().add_product(products[0]);
	                    self.clear_search();
	            	}else{
	            		products = _.filter(products, function (s) {
	                        return s != undefined;
	                    });
	                	self.product_list_widget.set_product_list(products, query);
	            	}
				});
				
        	}else{
            products = this.pos.db.get_product_by_category(this.category.id);
            this.product_list_widget.set_product_list(products, query);
        	}
		},
	});

});

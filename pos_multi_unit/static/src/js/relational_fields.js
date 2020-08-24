odoo.define('pos_multi_uom.relational_fields', function (require) {
    var relational_fields = require('web.relational_fields');
    var rpc = require('web.rpc');

    var _super = relational_fields.FieldMany2One.prototype._search;
    relational_fields.FieldMany2One.include({
        _search: function (search_val){
            var self = this;
            var def = $.Deferred();

            if (this.model === 'product.multi.uom') {
                var product_tmpl_id = this.get_current_id();
                if (!product_tmpl_id){
                    def.resolve();
                }
                var uom_id_field = _.clone(this.record.fields.uom_id);
                delete uom_id_field['domain'];


                rpc.query({
                    model: 'product.multi.uom',
                    method: 'get_uom_category_id',
                    args: [product_tmpl_id]
                }).then(function(category_id){
                    if (category_id) {
                        uom_id_field.domain = [["category_id", "=", category_id]];
                        self.record.fields.uom_id = uom_id_field;
                    }


                    def.resolve();
                });
            }else{
                def.resolve();
            }

            return def.then(function (){
                return _super.call(self, search_val);
            });
        },
         get_current_id: function () {
            var current_id = /#id=\d+/g.exec(window.location.href);
            if (!current_id) {
                return false;
            }
            var current_id = current_id[0].match(/\d+/g);
            if (!current_id) {
                return false;
            }
            return parseInt(current_id[0])
        }
    });
});
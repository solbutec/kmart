odoo.define('direct_printer.print', function (require) {
    'use strict';

    var ActionManager = require('web.ActionManager');
    var framework = require('web.framework');
    var session = require('web.session');
    var core = require('web.core');
    var _t = core._t;
    var _lt = core._lt;


    var wkhtmltopdf_state;

    var WKHTMLTOPDF_MESSAGES = {
        'install': _lt('Unable to find Wkhtmltopdf on this \nsystem. The report will be shown in html.<br><br><a href="http://wkhtmltopdf.org/" target="_blank">\nwkhtmltopdf.org</a>'),
        'workers': _lt('You need to start OpenERP with at least two \nworkers to print a pdf version of the reports.'),
        'upgrade': _lt('You should upgrade your version of\nWkhtmltopdf to at least 0.12.0 in order to get a correct display of headers and footers as well as\nsupport for table-breaking between pages.<br><br><a href="http://wkhtmltopdf.org/" \ntarget="_blank">wkhtmltopdf.org</a>'),
        'broken': _lt('Your installation of Wkhtmltopdf seems to be broken. The report will be shown in html.<br><br><a href="http://wkhtmltopdf.org/" target="_blank">wkhtmltopdf.org</a>')
    };

    var make_report_url = function (action) {
        var report_urls = {
            'qweb-html': '/report/html/' + action.report_name,
            'qweb-pdf': '/report/pdf/' + action.report_name,
        };

        if (_.isUndefined(action.data) || _.isNull(action.data) || (_.isObject(action.data) && _.isEmpty(action.data))) {
            if (action.context.active_ids) {
                var active_ids_path = '/' + action.context.active_ids.join(',');
                report_urls = _.mapObject(report_urls, function (value, key) {
                    return value += active_ids_path;
                });
            }
        } else {
            var serialized_options_path = '?options=' + encodeURIComponent(JSON.stringify(action.data));
            serialized_options_path += '&context=' + encodeURIComponent(JSON.stringify(action.context));
            report_urls = _.mapObject(report_urls, function (value, key) {
                return value += serialized_options_path;
            });
        }
        return report_urls;
    };

    ActionManager.include({
        ir_actions_report: function (action, options) {
            var current_action = _.clone(action);
            var self = this;

            if (action.report_type === 'qweb-pdf') {
                framework.blockUI();
                (wkhtmltopdf_state = wkhtmltopdf_state || this._rpc({route: '/report/check_wkhtmltopdf'})).then(function (state) {
                    if (WKHTMLTOPDF_MESSAGES[state]) {
                        self.do_notify(_t('Report'), WKHTMLTOPDF_MESSAGES[state], true);
                    }

                    if (state === 'upgrade' || state === 'ok') {
                        var report_urls = make_report_url(current_action);
                        window.open(session['web.base.url'] + report_urls['qweb-pdf']);
                        framework.unblockUI();
                    }
                });
            } else {
                return this._super.apply(this, [action, options]);
            }
        }
    });
});

odoo.define('employee.employee_information_report', function (require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var QWeb = core.qweb;

var EmployeeInformationReport = AbstractAction.extend({
    template: "EmployeeInformationReportTemplate",
    init: function (parent, params) {
        this._super.apply(this, arguments);
        this.row_click();
        if (params.context.data) {
            this.data = params.context.data;
        } else {
            this.data = [];
        }
    },

    //事件声明
    events: {},

    row_click: function () {
        var self = this;
        $('tr').delegate('.treeview-tr', 'click', function (e) {
            e.stopImmediatePropagation();
            var parent_id = $(this).parent().attr('id');
            $("[parent-id='" + parent_id + "']").each(function () {
                $(this).toggle();
            });

            if ($(this).parent().hasClass('oe_open')) {
                $(this).parent().removeClass('oe_open');
            } else {
                $(this).parent().addClass('oe_open');
            }

        });
    },

    start: function(){
    },
});
core.action_registry.add('employee_information_report_tag', EmployeeInformationReport);
return EmployeeInformationReport;
});



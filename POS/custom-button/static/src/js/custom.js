odoo.define('custom-button.custom_button', function (require) {
"use strict";

var core = require('web.core');
var screens = require('point_of_sale.screens');

var _t = core._t;

var ClearButton = screens.ActionButtonWidget.extend({
    template: 'ClearButton',
    button_click: function(){
        var self = this;
       this.gui.show_popup('confirm',{
                'title': _t('Destroy Current Order ?'),
                'body': _t('Are you Sure you want to Delete Current all Orders'),
                confirm: function(){
                    self.pos.delete_current_order();
                },
            });
    }
    
});

screens.define_action_button({
    'name': 'custom_button',
    'widget': ClearButton,
});


});

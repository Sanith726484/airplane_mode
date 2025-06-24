// Copyright (c) 2025, Sanith and contributors
// For license information, please see license.txt

frappe.ui.form.on('Airplane Ticket', {
    refresh: function(frm) {
        frm.add_custom_button(__('Assign Seat'), function() {
            frappe.prompt(
                [
                    {
                        label: 'Seat',
                        fieldname: 'seat',
                        fieldtype: 'Data',
                        reqd: true
                    }
                ],
                function(values) {
                    frm.set_value('seat', values.seat).then(() => {
                        frm.save().then(() => {
                            frappe.msgprint(__('Seat assigned successfully.'));
                        });
                    });
                },
                __('Select Seat'),
                __('Assign')
            );
        }, __('Actions'));
    }
});

// Copyright (c) 2025, Sanith and contributors
// For license information, please see license.txt

frappe.ui.form.on('Airplane Addon Item', {
    item: function(frm, cdt, cdn) {
        let current_row = locals[cdt][cdn];
        let selected_item = current_row.item;

        if (!selected_item) return;

        // Check if item already exists in another row
        let duplicate = frm.doc.add_on_items.some(row => {
            return row.item === selected_item && row.name !== current_row.name;
        });

        if (duplicate) {
            frappe.msgprint(__('This add-on item is already selected. Please choose a different one.'));
            frappe.model.set_value(cdt, cdn, 'item', null); // Clear the duplicate entry
        }
    }
});

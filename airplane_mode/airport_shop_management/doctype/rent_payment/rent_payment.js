// Copyright (c) 2025, Sanith and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rent Payment', {
    onload: function(frm) {
        frm.set_query('shop', function() {
            if (!frm.doc.contract) {
                frappe.msgprint(__('Please select a contract first.'));
                return { filters: { name: '__none' } };
            }

            return {
                query: "airplane_mode.airport_shop_management.doctype.airport_shop_contract.airport_shop_contract.get_contract_shops",
                filters: {
                    contract: frm.doc.contract
                }
            };
        });
    }
});

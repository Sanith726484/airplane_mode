frappe.ui.form.on('Shop Leads', {
    refresh: function(frm) {
        frm.add_custom_button("Create Contract", function () {
            frappe.model.with_doctype('Airport Shop Contract', function () {
                frappe.new_doc('Airport Shop Contract', {
                    tenant_name: frm.doc.tenant_name,
                    tenant_email: frm.doc.tenant_contact_email,
                });
            });
        });
    }
});

// Copyright (c) 2025, Sanith and contributors
// For license information, please see license.txt


frappe.ui.form.on('Airport Shop', {
  onload: function(frm) {
    frm.set_query("shop_type", function() {
      return {
        filters: {
          enabled: 1
        }
      };
    });
  }
});

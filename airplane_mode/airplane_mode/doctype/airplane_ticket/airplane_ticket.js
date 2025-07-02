// Copyright (c) 2025, Sanith and contributors
// For license information, please see license.txt

frappe.ui.form.on('Airplane Ticket', {
    refresh(frm) {
        frm.add_custom_button("Assign Seat",
            function() {
                frappe.prompt(
                    {
                        fieldname: 'seat',
                        label: 'Enter Seat Number',
                        fieldtype: 'Data',
                        reqd: 1
                    }, 
                    function(data) {
                        frm.set_value('seat', data.seat_number);
                        frm.save();
                        frappe.msgprint('Seat number assigned successfully.');
                    },
                    "Assign Seat Number"
                );
            },
            "Actions"
        );

        if (frm.doc.status === "Booked") {
            frm.add_custom_button ("Button name", function() {
                frm.set_value ("status", "Boarded")
                frm.save();
                frappe.msgprint('Ticket status updated to Boarded.');
            }, "Actions")
        }
    }


});

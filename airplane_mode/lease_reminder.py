from frappe.utils import getdate, add_days

def send_shop_lease_expiry_reminders():
    notify_date = add_days(getdate(), 7)

    contracts = frappe.get_all("Airport Shop Contract", filters={"docstatus": 1}, fields=["name", "tenant"])

    for contract in contracts:
        contract_doc = frappe.get_doc("Airport Shop Contract", contract.name)
        tenant_email = frappe.db.get_value("Airport Shop Tenant", contract_doc.tenant, "tenant_email")
        manager_email = frappe.db.get_single_value("Airport Shop Settings", "manager_email") or "defaultemiail@email.com"

        for shop_row in contract_doc.shops:
            if shop_row.end_date and getdate(shop_row.end_date) == notify_date:
                shop_name = frappe.db.get_value("Airport Shop", shop_row.shop, "shop_name")

                subject = f"Lease Expiry Reminder - {shop_name}"
                message = f"""
                Dear {contract_doc.tenant},

                This is a reminder that your lease for <b>{shop_name}</b> will expire on <b>{shop_row.end_date}</b>.

                Kindly get in touch if you wish to renew or vacate the shop.

                Regards,<br>
                Airport Management
                """

                try:
                    frappe.sendmail(
                        recipients=[tenant_email],
                        cc=[manager_email],
                        subject=subject,
                        message=message
                    )
                    frappe.logger().info(f"Reminder sent for shop {shop_row.shop}")
                except Exception as e:
                    frappe.logger().error(f"Failed to send reminder for {shop_row.shop}: {str(e)}")

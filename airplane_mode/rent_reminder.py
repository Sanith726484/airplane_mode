import frappe
from frappe.utils import getdate, nowdate, formatdate

def send_rent_due_reminders():
    settings = frappe.get_single("Airport Shop Settings")
    if not settings.enable_rent_reminders:
        print("Rent reminders disabled in settings.")
        return

    today = getdate(nowdate())
    current_month = today.strftime("%Y-%m-%d")
    print(f"Running rent reminder check for month: {current_month}")

    contracts = frappe.get_all(
        "Airport Shop Contract",
        filters={"docstatus": 1},
        fields=["name", "tenant_name", "tenant_email"]
    )

    print(f"Found {len(contracts)} active contracts.")

    reminders_sent = 0
    for contract in contracts:
        if not contract.tenant_email:
            print(f"Skipping contract {contract.name} (no email provided)")
            continue

        contract_doc = frappe.get_doc("Airport Shop Contract", contract.name)

        for shop_entry in contract_doc.shops:
            shop_id = shop_entry.shop
            rent = shop_entry.monthly_rent
            lease_start = getdate(shop_entry.start_date)
            lease_end = getdate(shop_entry.end_date)

            if not (lease_start <= today <= lease_end):
                print(f"Shop {shop_id} in contract {contract.name} not active this month.")
                continue

            rent_paid = frappe.get_all(
                "Rent Payment",
                filters={
                    "contract": contract.name,
                    "shop": shop_id,
                    "month": ["like", f"{current_month}"],
                    "status": "Paid"
                },
                limit=1
            )

            if rent_paid:
                print(f"Payment already made for Shop {shop_id}, contract {contract.name}.")
                continue

            # Send reminder
            subject = f"Rent Due Reminder for {formatdate(today, 'MMMM YYYY')} - Shop {shop_id} in {contract.name}"
            message = f"""
                Dear {contract.tenant_name},<br><br>
                This is a reminder that your rent of <strong>{rent} USD</strong> 
                for <strong>Shop {shop_id}</strong> for the month of <strong>{formatdate(today, 'MMMM YYYY')}</strong> is due.<br><br>
                Please ensure the payment is made on time.<br><br>
                Regards,<br>
                Airport Authority
            """

            try:
                frappe.sendmail(
                    recipients=[contract.tenant_email],
                    subject=subject,
                    message=message,
                    delayed=True
                )
                print(f"Reminder sent to {contract.tenant_email} for Shop {shop_id} in contract {contract.name}")
                reminders_sent += 1
            except Exception as e:
                print(f"Failed to send email to {contract.tenant_email}: {e}")

    print(f"✅ Total reminders sent: {reminders_sent}")
    frappe.db.commit()


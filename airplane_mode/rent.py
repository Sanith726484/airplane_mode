import frappe
from frappe.utils import today, nowdate, getdate
from datetime import datetime

def send_rent_reminders():
    settings = frappe.get_single("Airport Shop Settings")
    if not settings.enable_rent_reminders:
        return

    current_month = datetime.today().strftime("%b")
    current_year = datetime.today().year

    shops = frappe.get_all("Airport Shop", filters={"status": "Occupied"}, fields=["shop_name", "tenant_email", "monthly_rent"])

    for shop in shops:
        # Check if payment exists
        exists = frappe.db.exists("Rent Payment", {
            "shop": shop.shop_name,
            "month": current_month,
            "year": current_year
        })

        if not exists and shop.tenant_email:
            frappe.sendmail(
                recipients=[shop.tenant_email],
                subject=f"Rent Due Reminder - {current_month} {current_year}",
                message=f"Dear Tenant, your rent of ₹{shop.monthly_rent} for Shop {shop.shop_name} is due. Please make the payment at the earliest."
            )

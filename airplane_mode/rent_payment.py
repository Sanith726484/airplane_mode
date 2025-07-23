import frappe
from frappe.utils import get_first_day, getdate
from datetime import timedelta

def create_monthly_rent_payments():
    today = getdate() + timedelta(days=1)
    month_start = get_first_day(today)

    contracts = frappe.get_all("Airport Shop Contract", filters={"docstatus": 1})

    for contract in contracts:
        contract_doc = frappe.get_doc("Airport Shop Contract", contract.name)
        # print(f"\n📄 Processing Contract: {contract_doc.name}")

        for shop_entry in contract_doc.shops:
            shop = shop_entry.shop
            tenant = contract_doc.tenant_name
            rent_amount = shop_entry.monthly_rent

            if getdate(shop_entry.end_date) < today:
                # print(f"⏭️  Skipping expired lease for shop: {shop}")
                continue

            existing = frappe.db.exists(
                "Rent Payment",
                {
                    "shop": shop,
                    "tenant_name": tenant,
                    "contract": contract_doc.name,
                    "month": month_start,
                }
            )

            if existing:
                print(f"✅ Already exists for shop {shop}, month {month_start}")
                continue

            month_str = month_start.strftime("%Y-%m")
            custom_name = f"RP-{contract_doc.name}-{shop}-{month_str}"

            # print(f"🆕 Creating Rent Payment with name: {custom_name}")

            for attempt in range(3):
                try:
                    rent_payment = frappe.get_doc({
                        "doctype": "Rent Payment",
                        "name": custom_name,
                        "shop": shop,
                        "tenant_name": tenant,
                        "contract": contract_doc.name,
                        "month": month_start,
                        "amount": rent_amount,
                        "payment_status": "Pending"
                    })
                    rent_payment.insert(ignore_permissions=True, ignore_if_duplicate=True)
                    print(f"✅ Inserted: {custom_name}")
                    break
                except Exception as e:
                    print(f"❌ Failed to insert {custom_name}: {e}")
                    break
            frappe.db.commit()


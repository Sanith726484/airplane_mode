from frappe.utils import getdate, today

def update_expired_shops_individually():
    today_date = getdate()

    all_contracts = frappe.get_all("Airport Shop Contract", filters={"docstatus": 1}, fields=["name"])
    for contract in all_contracts:
        contract_doc = frappe.get_doc("Airport Shop Contract", contract.name)

        for shop_row in contract_doc.shops:
            if shop_row.end_date and getdate(shop_row.end_date) < today_date:
                shop = frappe.get_doc("Airport Shop", shop_row.shop)
                if shop.status != "Available":
                    shop.status = "Available"
                    shop.save(ignore_permissions=True)

import frappe

def execute():
    contracts = frappe.get_all("Airport Shop Contract", filters={"docstatus": 1}, fields=["name"])
    total_updated = 0

    for contract in contracts:
        shops = frappe.get_all(
            "Airport Contract Shops",
            filters={"parent": contract.name},
            fields=["shop"]
        )

        for shop_row in shops:
            shop = frappe.get_doc("Airport Shop", shop_row.shop)
            if shop.status != "Occupied":
                shop.status = "Occupied"
                shop.save(ignore_permissions=True)
                total_updated += 1

    frappe.logger().info(f"✅ Patch completed: {total_updated} shops marked as Occupied.")

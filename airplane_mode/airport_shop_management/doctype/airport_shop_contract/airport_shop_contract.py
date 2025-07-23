# Copyright (c) 2025, Sanith and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AirportShopContract(Document):
    def validate(self):
        self.calculate_total_monthly_rent()

    def on_submit(self):
        self.mark_shops_as_occupied()    
    
    def on_cancel(self):
        # Reset shop statuses to "Available" when contract is cancelled
        for shop_row in self.shops:
            shop = frappe.get_doc("Airport Shop", shop_row.shop)
            if shop.status == "Occupied":
                shop.status = "Available"
                shop.save(ignore_permissions=True)

    def calculate_total_monthly_rent(self):
        total = 0
        for shop_row in self.shops:
            shop = frappe.get_doc("Airport Shop", shop_row.shop)
            total += shop.monthly_rent or 0

        self.total_monthly_rent = total

    def mark_shops_as_occupied(self):
        for shop_row in self.shops:
            shop = frappe.get_doc("Airport Shop", shop_row.shop)
            shop.status = "Occupied"
            shop.save(ignore_permissions=True)

@frappe.whitelist()
def get_contract_shops(doctype, txt, searchfield, start, page_len, filters):
	contract = filters.get("contract")
	if not contract:
		return []

	shop_links = frappe.get_all(
		"Airport Contract Shops",
		filters={"parent": contract},
		fields=["shop"]
	)

	return [(s.shop,) for s in shop_links if s.shop]
	
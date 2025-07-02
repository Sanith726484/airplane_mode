# Copyright (c) 2025, Sanith and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AirportShopContract(Document):
	def validate(self):
		self.calculate_total_monthly_rent()

	def calculate_total_monthly_rent(self):
		total =  0
		for shop_row in self.shops:
			shop = frappe.get_doc("Airport Shop", shop_row.shop)
			total += shop.monthly_rent or 0

		self.total_monthly_rent = total

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
	
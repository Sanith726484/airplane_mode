# Copyright (c) 2025, Sanith and contributors
# For license information, please see license.txt

from datetime import datetime
import frappe
from frappe.model.document import Document


class RentPayment(Document):

	def validate(self):
		today_str = datetime.today().strftime('%Y-%m-%d')
		count = frappe.db.count("Rent Payment", {"creation": ["like", today_str + "%"]})
		sequence = f"{count + 1:03}"

		self.receipt_number = f"{today_str}-{sequence}"
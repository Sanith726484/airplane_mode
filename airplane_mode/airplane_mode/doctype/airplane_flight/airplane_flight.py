# Copyright (c) 2025, Sanith and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe import enqueue


class AirplaneFlight(WebsiteGenerator):
	def on_submit(self):
		self.status = "Completed"

	def on_update(self):
		if self.has_value_changed("gate_number"):
			frappe.enqueue(
				update_gate_number_in_tickets,
				queue='default',
				flight_name=self.name,
				gate_number=self.gate_number
			)

def update_gate_number_in_tickets(flight_name: str, gate_number: str):
	tickets = frappe.get_all("Airplane Ticket", filters={"flight": flight_name}, fields=["name"])

	for ticket in tickets:
		frappe.db.set_value("Airplane Ticket", ticket.name, "gate_number", gate_number)

# Copyright (c) 2025, Sanith and contributors
# For license information, please see license.txt
import frappe
import random
from frappe import _
from frappe.website.website_generator import WebsiteGenerator

class AirplaneTicket(WebsiteGenerator):
	
	def before_insert(self):
		number = random.randint(1, 99)
		letter = random.choice(['A', 'B', 'C', 'D', 'E'])
		self.seat = f"{number}{letter}"
		self.check_flight_capacity()
		gate_number = frappe.db.get_value("Airplane Flight", self.flight, "gate_number")
		self.gate_number = f"{gate_number}"
	
	def on_submit(self):
		if self.status != "Boarded":
			frappe.throw(_("Cannot submit the ticket unless status is 'Boarded'."), frappe.ValidationError)

	def validate(self):
		self.remove_duplicate_add_ons()
		self.set_total_amount()

	def remove_duplicate_add_ons(self):
		seen = set()
		unique_add_ons = []

		for row in self.add_ons:
			if row.item not in seen:
				seen.add(row.item)
				unique_add_ons.append(row)

		if len(unique_add_ons) < len(self.add_ons):
			self.add_ons = unique_add_ons
			frappe.msgprint("Duplicate add-ons were removed. Only unique items are allowed.")

	def set_total_amount(self):
		flight_price = self.flight_price or 0
		total_add_ons = sum((row.amount or 0) for row in self.add_ons)
		print(f"Flight Price: {flight_price}, Total Add-Ons: {total_add_ons}")
		self.total_amount = float(flight_price) + float(total_add_ons)

	def check_flight_capacity(self):
		if not self.flight:
			return

		try:
			flight_doc = frappe.get_doc("Airplane Flight", self.flight)

			if not flight_doc.airplane:
				return

			capacity = frappe.db.get_value("Airplane", flight_doc.airplane, "capacity") or 0

			ticket_count = frappe.db.count("Airplane Ticket", {"flight": self.flight})

			if ticket_count >= capacity:
				raise ValidationError(
					_("Cannot create ticket. Flight '{0}' has reached its full capacity of {1} seats.")
					.format(self.flight, capacity)
				)

		except ValidationError as exc:
			frappe.throw(str(exc), frappe.ValidationError)

# Copyright (c) 2025, Sanith and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe import _

class Airline(WebsiteGenerator):
	
	def get_context(self, context):
		# If the website field is set, redirect to it
		if self.website:
			frappe.local.flags.redirect_location = self.website
			raise frappe.Redirect

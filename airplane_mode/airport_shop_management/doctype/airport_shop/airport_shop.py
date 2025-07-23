# Copyright (c) 2025, Sanith and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class AirportShop(WebsiteGenerator):
    def on_submit(self):
        self.is_published = 1

    def validate(self):
        if not self.monthly_rent:
            settings = frappe.get_single("Airport Shop Settings")
            self.monthly_rent = settings.default_monthly_rent or 0

        if not self.route:
            self.route = f"shops/{self.shop_name.strip().lower().replace(' ', '-')}"

# Copyright (c) 2025, Sanith and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.query_builder import DocType, functions as fn
from frappe.query_builder.functions import Count, Sum, If
from frappe import qb

def execute(filters: dict | None = None):
	"""Return columns and data for the report.

	This is the main entry point for the report. It accepts the filters as a
	dictionary and should return columns and data. It is called by the framework
	every time the report is refreshed or a filter is updated.
	"""
	columns = get_columns()
	data = get_data()

	return columns, data


def get_columns() -> list[dict]:
	"""Return columns for the report.

	One field definition per column, just like a DocType field definition.
	"""
	return [
		{
			"label": _("Airport"),
			"fieldname": "airport",
			"fieldtype": "link",
		},
		{
			"label": _("Total Shops"),
			"fieldname": "total",
			"fieldtype": "Int",
		},
		{
			"label": _("occupied Shops"),
			"fieldname": "occupied",
			"fieldtype": "Int",
		},
		{
			"label": _("Available Shops"),
			"fieldname": "available",
			"fieldtype": "Int",
		}
	]


def get_data() -> list[list]:

	AirportShop = DocType("Airport Shop")

	occupied_case = (
        qb.case()
        .when(AirportShop.tenant_name.isnotnull() & (AirportShop.tenant_name != ""), 1)
        .else_(0)
    )

	available_case = (
        qb.case()
        .when(AirportShop.tenant_name.isnull() | (AirportShop.tenant_name == ""), 1)
        .else_(0)
    )

	result = (
        qb.from_(AirportShop)
        .select(
            AirportShop.airport.as_("airport"),
            Count("*").as_("total"),
            occupied_case.sum().as_("occupied"),
            available_case.sum().as_("available"),
        )
        .groupby(AirportShop.airport)
    ).run(as_dict=True)

	return result

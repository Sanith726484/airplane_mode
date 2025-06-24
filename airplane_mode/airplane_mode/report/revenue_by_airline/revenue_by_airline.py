# Copyright (c) 2025, Sanith and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.query_builder import DocType, functions as fn
from frappe import qb


def execute(filters: dict | None = None):
	columns = [
		{
			"label": _("Airline"),
			"fieldname": "airline",
			"fieldtype": "Link",
			"options": "Airline",
		},
		{
			"label": _("Revenue"),
			"fieldname": "total_revenue",
			"fieldtype": "Currency",
		},
	]

	data = get_data()

	total_revenue = sum(row["total_revenue"] for row in data)

	chart = {
		"data": {
			"labels": [d["airline"] for d in data],
			"datasets": [
				{
					"name": _("Total Revenue"),
					"values": [d["total_revenue"] for d in data]
				}
			]
		},
		"type": "donut"
	}

	# Report Summary (top section)
	report_summary = [
		{
			"value": total_revenue,
			"label": _("Total Revenue"),
			"indicator": "Green"
		}
	]

	# Total row (footer)
	total_row = {
		"airline": _("Total"),
		"total_revenue": total_revenue
	}

	data.append(total_row)

	return columns, data, "Report", chart, report_summary


def get_data() -> list[dict]:
	Airplane = DocType("Airplane")
	AirplaneFlight = DocType("Airplane Flight")
	AirplaneTicket = DocType("Airplane Ticket")

	result = (
		qb.from_(Airplane)
		.left_join(AirplaneFlight).on(AirplaneFlight.airplane == Airplane.name)
		.left_join(AirplaneTicket).on(AirplaneTicket.flight == AirplaneFlight.name)
		.groupby(Airplane.airline)
		.select(
			Airplane.airline.as_("airline"),
			fn.Sum(AirplaneTicket.total_amount).as_("total_revenue")
		)
	).run(as_dict=True)

	# Ensure no None values
	for row in result:
		row["total_revenue"] = row["total_revenue"] or 0

	return result

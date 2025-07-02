import frappe

def get_context(context):
    context.flights = frappe.get_all(
        "Airplane Flight",
        fields=["name", "source_airport_code", "destination_airport_code", "date_of_departure", "route"],
        limit=10,
        order_by="date_of_departure desc"
    )

    context.shops = frappe.get_all(
        "Airport Shop",
        filters={"is_published": 1},
        fields=["shop_name", "status", "route"],
        limit=10
    )

import frappe

def execute():
    flights = frappe.get_all(
        "Airplane Flight",
        filters={"docstatus": 1},
        fields=["name", "is_published"]
    )

    print("Submitted Airplane Flights:")
    for flight in flights:
        print(f" - {flight['name']}")


    for flight in flights:
        if not flight.is_published:
            doc = frappe.get_doc("Airplane Flight", flight.name)
            doc.is_published = 1
            doc.save(ignore_permissions=True)
            frappe.logger().info(f"✅ Published flight: {flight.name}")

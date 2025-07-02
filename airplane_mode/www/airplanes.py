import frappe

def get_context(context):
    airplanes = frappe.get_all("Airplane", fields=["name", "model", "airline"])

    context.airplanes = airplanes
    return context

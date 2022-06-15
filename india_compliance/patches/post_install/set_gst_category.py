import frappe


def execute():
    invoice_type_gst_category_map = {
        "Regular": "Registered Regular",
        "Export": "Overseas",
        "SEZ": "SEZ",
        "Deemed Export": "Deemed Export",
    }

    for doctype in ("Sales Invoice", "Purchase Invoice"):
        field_filters = {"dt": doctype, "fieldname": "invoice_type"}

        if not frappe.db.exists("Custom Field", field_filters):
            continue

        for invoice_type, gst_category in invoice_type_gst_category_map.items():
            frappe.db.set(
                doctype,
                {"gst_category": ("in", (None, "")), "invoice_type": invoice_type},
                "gst_category",
                gst_category,
            )

        frappe.db.delete("Custom Field", field_filters)

    # update eligibility_for_itc with new options
    for old_value, new_value in {
        "ineligible": "Ineligible",
        "input service": "Input Service Distributor",
        "capital goods": "Import Of Capital Goods",
        "input": "All Other ITC",
    }.items():
        frappe.db.set_value(
            "Purchase Invoice",
            {"eligibility_for_itc": old_value},
            "eligibility_for_itc",
            new_value,
        )

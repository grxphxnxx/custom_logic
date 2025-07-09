import frappe
from frappe.model.naming import make_autoname

def autoname(doc, method):
    choice = doc.get("proj_ns_choice")

    config = {
        "Auftrag neu":    ("A-", 6347, 3),
        "Reparatur neu": ("R-", 4324, 2),
        "Ersatzteil neu":("E-", 2000, 5),
        "MFK neu":       ("M-", 900, 10),
    }

    if choice in config:
        prefix, start, step = config[choice]
        counter_key = f"project_custom_{prefix.rstrip('-').lower()}"

        current = frappe.db.get_single_value("Custom Naming Counter", counter_key) or start - step
        next_val = int(current) + step

        name = f"{prefix}{next_val}"
        doc.name = name

        if not frappe.db.exists("Custom Naming Counter"):
            doc = frappe.get_doc({"doctype": "Custom Naming Counter"})
            doc[counter_key] = next_val
            doc.insert()
        else:
            frappe.db.set_value("Custom Naming Counter", None, counter_key, next_val)

    elif choice == "Manuelle Eingabe":
        pass
    else:
        doc.name = make_autoname("PROJ-.####")

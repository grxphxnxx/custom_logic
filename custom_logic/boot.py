import frappe

def enable_server_scripts():
    """Server Scripts automatisch aktivieren"""
    frappe.db.set_single_value("System Settings", "allow_server_script_change", 1)
    frappe.db.set_single_value("System Settings", "server_script_enabled", 1)
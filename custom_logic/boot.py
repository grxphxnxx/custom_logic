# custom_logic/boot.py
import frappe

def enable_server_scripts(bootinfo):
    """Server Scripts automatisch aktivieren - Parameter für Boot Hook nötig"""
    try:
        # Prüfen ob bereits aktiviert
        current_settings = frappe.get_single("System Settings")
        
        if not current_settings.get("server_script_enabled"):
            frappe.db.set_single_value("System Settings", "server_script_enabled", 1)
            
        if not current_settings.get("allow_server_script_change"):
            frappe.db.set_single_value("System Settings", "allow_server_script_change", 1)
            
        frappe.db.commit()
        
    except Exception as e:
        # Fehler loggen aber nicht werfen (um Boot nicht zu blockieren)
        frappe.log_error(f"Server Scripts Aktivierung fehlgeschlagen: {str(e)}")
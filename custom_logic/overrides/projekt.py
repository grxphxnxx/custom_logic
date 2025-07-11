# custom_logic/overrides/projekt.py
import frappe
from frappe.model.naming import make_autoname

def autoname(doc, method):
    """Custom Autoname für Projekte"""
    if not doc.naming_series:
        return
        
    series_config = {
        'A-.####': {'prefix': 'A', 'increment': 3, 'start': 7435},
        'R-.####': {'prefix': 'R', 'increment': 2, 'start': 1000}, 
        'E-.####': {'prefix': 'E', 'increment': 1, 'start': 1000},
        'M-.####': {'prefix': 'M', 'increment': 2, 'start': 1000}
    }
    
    if doc.naming_series in series_config:
        config = series_config[doc.naming_series]
        
        # Höchste Nummer finden
        result = frappe.db.sql("""
            SELECT MAX(CAST(SUBSTRING(name, 3) AS UNSIGNED)) as max_num
            FROM `tabProject` 
            WHERE name LIKE %s
        """, (f"{config['prefix']}-%",))
        
        current_max = result[0][0] if result[0][0] else config['start'] - config['increment']
        next_num = current_max + config['increment']
        
        doc.name = f"{config['prefix']}-{next_num:04d}"
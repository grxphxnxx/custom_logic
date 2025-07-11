# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe

def execute():
    """Custom Felder zum Project DocType hinzufügen"""
    
    # Custom Felder zum Hinzufügen
    custom_felder = [
        {
            'fieldname': 'proj_ns_choice',
            'label': 'Namensserien Auswahl',
            'fieldtype': 'Select',
            'options': 'auftrag_neu\nreparatur_neu\nersatzteil_neu\nmfk_neu\nmanual',
            'insert_after': 'project_name',
            'in_list_view': 1,
            'reqd': 1,
            'description': 'Wählen Sie die Namensserie oder manuelle Eingabe'
        }
    ]
    
    for feld_konfiguration in custom_felder:
        if not frappe.db.exists('Custom Field', {'dt': 'Project', 'fieldname': feld_konfiguration['fieldname']}):
            custom_field = frappe.new_doc('Custom Field')
            custom_field.dt = 'Project'
            custom_field.update(feld_konfiguration)
            custom_field.insert()
            print(f"Custom Field hinzugefügt: {feld_konfiguration['fieldname']}")
        else:
            print(f"Custom Field existiert bereits: {feld_konfiguration['fieldname']}")
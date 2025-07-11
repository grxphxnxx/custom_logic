# -*- coding: utf-8 -*-
import frappe
import json
from frappe.utils import now

@frappe.whitelist()
def exportiere_namensserien_konfiguration():
    """Alle Namensserien Konfigurationen exportieren"""
    serien_liste = frappe.get_all('Projekt Namensserie', 
                                 fields=['*'])
    
    export_daten = {
        'zeitstempel': now(),
        'version': '1.0',
        'namensserien': serien_liste
    }
    
    return export_daten

@frappe.whitelist()
def importiere_namensserien_konfiguration(import_daten):
    """Namensserien Konfigurationen importieren"""
    if not isinstance(import_daten, dict):
        import_daten = json.loads(import_daten)
    
    for serien_konfiguration in import_daten.get('namensserien', []):
        existiert = frappe.db.exists('Projekt Namensserie', serien_konfiguration.get('name'))
        
        if existiert:
            doc = frappe.get_doc('Projekt Namensserie', existiert)
            doc.update(serien_konfiguration)
            doc.save()
        else:
            doc = frappe.new_doc('Projekt Namensserie')
            doc.update(serien_konfiguration)
            doc.insert()
    
    return {"status": "erfolgreich", "nachricht": "Import abgeschlossen"}

@frappe.whitelist()
def erstelle_backup_aller_projektdaten():
    """Vollständiges Backup aller projektrelevanten Daten"""
    backup_daten = {
        'zeitstempel': now(),
        'version': '1.0',
        'namensserien': frappe.get_all('Projekt Namensserie', fields=['*']),
        'custom_fields': frappe.get_all('Custom Field', 
                                       filters={'dt': 'Project'},
                                       fields=['*']),
        'projekte': frappe.get_all('Project', 
                                  fields=['name', 'custom_project_id', 'proj_ns_choice'])
    }
    
    return backup_daten
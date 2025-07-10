# -*- coding: utf-8 -*-
# Copyright (c) 2024, Ihr Unternehmen and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ProjektNamensserie(Document):
    def validate(self):
        """Validierung der Naming Series Konfiguration"""
        if self.increment_by <= 0:
            frappe.throw("Inkrement muss größer als 0 sein")
        
        if self.aktuelle_nummer < 0:
            frappe.throw("Aktuelle Nummer kann nicht negativ sein")
        
        # Präfix Format validieren
        if not self.prefix or len(self.prefix) != 1:
            frappe.throw("Präfix muss ein einzelnes Zeichen sein (A, R, E, oder M)")
        
        gueltige_praefix = ['A', 'R', 'E', 'M']
        if self.prefix not in gueltige_praefix:
            frappe.throw(f"Präfix muss eines der folgenden sein: {', '.join(gueltige_praefix)}")
    
    def get_next_number(self):
        """Nächste Nummer in der Serie holen und aktuelle Nummer erhöhen"""
        naechste_nummer = self.aktuelle_nummer + self.increment_by
        self.aktuelle_nummer = naechste_nummer
        self.save()
        return naechste_nummer
    
    def get_formatted_name(self, nummer=None):
        """Formatierte Bezeichnung mit der Serienkonfiguration erstellen"""
        if nummer is None:
            nummer = self.get_next_number()
        return f"{self.prefix}-{nummer:04d}"

@frappe.whitelist()
def get_next_project_name(series_name):
    """Nächste Projektbezeichnung für eine gegebene Serie holen"""
    try:
        serie = frappe.get_doc("Projekt Namensserie", series_name)
        if not serie.is_active:
            frappe.throw(f"Serie {series_name} ist nicht aktiv")
        
        return serie.get_formatted_name()
    except Exception as e:
        frappe.log_error(f"Fehler beim Generieren der Projektbezeichnung: {str(e)}")
        frappe.throw(f"Fehler beim Generieren der Projektbezeichnung: {str(e)}")

@frappe.whitelist()
def get_available_series():
    """Alle verfügbaren aktiven Naming Series holen"""
    serien = frappe.get_all("Projekt Namensserie", 
                           filters={"is_active": 1},
                           fields=["series_name", "series_label", "prefix"])
    return serien

@frappe.whitelist()
def validate_manual_name(projekt_name):
    """Manuell eingegebene Projektbezeichnung validieren"""
    if not projekt_name:
        return {"valid": False, "message": "Projektname kann nicht leer sein"}
    
    # Format prüfen: X-XXXX
    if len(projekt_name) < 6 or projekt_name[1] != '-':
        return {"valid": False, "message": "Format muss X-XXXX sein (z.B. A-0001)"}
    
    prefix = projekt_name[0]
    nummer_teil = projekt_name[2:]
    
    # Präfix validieren
    gueltige_praefix = ['A', 'R', 'E', 'M']
    if prefix not in gueltige_praefix:
        return {"valid": False, "message": f"Präfix muss eines der folgenden sein: {', '.join(gueltige_praefix)}"}
    
    # Nummer Teil validieren
    if not nummer_teil.isdigit():
        return {"valid": False, "message": "Nummerteil darf nur Ziffern enthalten"}
    
    # Prüfen ob Name bereits existiert
    existiert = frappe.db.exists("Project", projekt_name)
    if existiert:
        return {"valid": False, "message": "Projektname existiert bereits"}
    
    return {"valid": True, "message": "Gültiger Projektname"}
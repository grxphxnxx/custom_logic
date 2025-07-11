# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import _

def before_insert(doc, method):
    """Projektbenennung vor dem Einfügen handhaben"""
    if not doc.name or doc.name.startswith('new-project'):
        generiere_projekt_name(doc)

def validate(doc, method):
    """Projektbenennung validieren"""
    if hasattr(doc, 'proj_ns_choice') and doc.proj_ns_choice:
        if doc.proj_ns_choice == 'manual':
            validiere_manuellen_projekt_name(doc)
        else:
            # Sicherstellen dass der Name dem Serienmuster folgt
            validiere_serien_projekt_name(doc)

def generiere_projekt_name(doc):
    """Projektname basierend auf Naming Series Auswahl generieren"""
    if not hasattr(doc, 'proj_ns_choice') or not doc.proj_ns_choice:
        return
    
    if doc.proj_ns_choice == 'manual':
        # Manuelle Benennung - Benutzer muss 'name' direkt setzen
        return  # name wird vom Benutzer eingegeben
    
    # Auto-generieren aus Serie
    try:
        from custom_logic.custom_logic.doctype.projekt_namensserie.projekt_namensserie import get_next_project_name
        doc.name = get_next_project_name(doc.proj_ns_choice)
    except Exception as e:
        frappe.log_error(f"Fehler beim Generieren des Projektnamens: {str(e)}")
        frappe.throw(_("Fehler beim Generieren des Projektnamens."))

def validiere_manuellen_projekt_name(doc):
    """Manuell eingegebenen Projektname validieren"""
    if not doc.name:
        frappe.throw(_("Projektname ist erforderlich"))
    
    from custom_logic.custom_logic.doctype.projekt_namensserie.projekt_namensserie import validate_manual_name
    validierungs_ergebnis = validate_manual_name(doc.name)
    
    if not validierungs_ergebnis.get('valid'):
        frappe.throw(validierungs_ergebnis.get('message', 'Ungültiger Projektname'))

def validiere_serien_projekt_name(doc):
    """Serien-generierten Projektname validieren"""
    if not doc.name:
        return
    
    # Prüfen ob der Name dem erwarteten Muster folgt
    if len(doc.name) < 6 or doc.name[1] != '-':
        frappe.throw(_("Projektname muss dem Format X-XXXX folgen"))
    
    prefix = doc.name[0]
    gueltige_praefix = ['A', 'R', 'E', 'M']
    if prefix not in gueltige_praefix:
        frappe.throw(_("Projektname Präfix muss eines der folgenden sein: A, R, E, M"))
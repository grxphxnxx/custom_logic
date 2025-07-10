# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe

def execute():
    """Standard Projekt Naming Series erstellen"""
    
    # Standard Serien Konfigurationen
    serien_konfigurationen = [
        {
            'series_name': 'auftrag_neu',
            'series_label': 'Auftrag neu',
            'prefix': 'A',
            'aktuelle_nummer': 7435,
            'increment_by': 3,
            'beschreibung': 'Neue Aufträge - jede 3. Nummer'
        },
        {
            'series_name': 'reparatur_neu',
            'series_label': 'Reparatur neu',
            'prefix': 'R',
            'aktuelle_nummer': 1000,
            'increment_by': 2,
            'beschreibung': 'Neue Reparaturen - jede 2. Nummer'
        },
        {
            'series_name': 'ersatzteil_neu',
            'series_label': 'Ersatzteil neu',
            'prefix': 'E',
            'aktuelle_nummer': 1000,
            'increment_by': 1,
            'beschreibung': 'Neue Ersatzteile - jede Nummer'
        },
        {
            'series_name': 'mfk_neu',
            'series_label': 'MFK neu',
            'prefix': 'M',
            'aktuelle_nummer': 1000,
            'increment_by': 2,
            'beschreibung': 'Neue MFK - jede 2. Nummer'
        }
    ]
    
    for konfiguration in serien_konfigurationen:
        if not frappe.db.exists('Projekt Namensserie', konfiguration['series_name']):
            doc = frappe.new_doc('Projekt Namensserie')
            doc.update(konfiguration)
            doc.is_active = 1
            doc.insert()
            print(f"Namensserie erstellt: {konfiguration['series_name']}")
        else:
            print(f"Namensserie existiert bereits: {konfiguration['series_name']}")
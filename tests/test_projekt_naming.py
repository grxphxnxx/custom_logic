# -*- coding: utf-8 -*-
import frappe
import unittest
from custom_logic.custom_logic.doctype.projekt_namensserie.projekt_namensserie import get_next_project_name, validate_manual_name

class TestProjektNaming(unittest.TestCase):
    def setUp(self):
        # Test Namensserie erstellen
        if not frappe.db.exists('Projekt Namensserie', 'test_serie'):
            doc = frappe.new_doc('Projekt Namensserie')
            doc.series_name = 'test_serie'
            doc.series_label = 'Test Serie'
            doc.prefix = 'T'
            doc.aktuelle_nummer = 1000
            doc.increment_by = 1
            doc.is_active = 1
            doc.insert()
    
    def test_naechste_name_generierung(self):
        """Test der Namen-Generierung"""
        name = get_next_project_name('test_serie')
        self.assertTrue(name.startswith('T-'))
        self.assertTrue(len(name) >= 6)
    
    def test_manuelle_name_validierung(self):
        """Test der manuellen Namen-Validierung"""
        # Gültiger Name
        result = validate_manual_name('A-1234')
        self.assertTrue(result['valid'])
        
        # Ungültiger Name
        result = validate_manual_name('X-1234')
        self.assertFalse(result['valid'])
    
    def test_inkrement_funktionalitaet(self):
        """Test der Inkrement-Funktionalität"""
        serie = frappe.get_doc('Projekt Namensserie', 'test_serie')
        alte_nummer = serie.aktuelle_nummer
        naechste_nummer = serie.get_next_number()
        self.assertEqual(naechste_nummer, alte_nummer + serie.increment_by)
    
    def tearDown(self):
        # Test-Daten aufräumen
        if frappe.db.exists('Projekt Namensserie', 'test_serie'):
            frappe.delete_doc('Projekt Namensserie', 'test_serie')
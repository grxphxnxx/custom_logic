// Copyright (c) 2024, Ihr Unternehmen and contributors
// For license information, please see license.txt

frappe.ui.form.on('Projekt Namensserie', {
    refresh: function(frm) {
        // Custom Buttons hinzufügen
        frm.add_custom_button(__('Nächste Nummer testen'), function() {
            teste_naechste_nummer(frm);
        });
        
        frm.add_custom_button(__('Zähler zurücksetzen'), function() {
            zaehler_zuruecksetzen(frm);
        });
    },
    
    prefix: function(frm) {
        // Standard Inkrement basierend auf Präfix setzen
        if (!frm.doc.increment_by || frm.doc.increment_by === 1) {
            const inkremente = {
                'A': 3,  // jede 3. Nummer
                'R': 2,  // jede 2. Nummer
                'E': 1,  // jede Nummer
                'M': 2   // jede 2. Nummer
            };
            frm.set_value('increment_by', inkremente[frm.doc.prefix] || 1);
        }
    },
    
    series_name: function(frm) {
        // Auto-generiere series_label wenn nicht gesetzt
        if (!frm.doc.series_label && frm.doc.series_name) {
            const labels = {
                'auftrag_neu': 'Auftrag neu',
                'reparatur_neu': 'Reparatur neu',
                'ersatzteil_neu': 'Ersatzteil neu',
                'mfk_neu': 'MFK neu'
            };
            frm.set_value('series_label', labels[frm.doc.series_name] || frm.doc.series_name);
        }
    }
});

function teste_naechste_nummer(frm) {
    if (!frm.doc.name) {
        frappe.msgprint(__('Bitte speichern Sie das Dokument zuerst'));
        return;
    }
    
    frappe.call({
        method: 'custom_logic.custom_logic.doctype.projekt_namensserie.projekt_namensserie.get_next_project_name',
        args: {
            series_name: frm.doc.name
        },
        callback: function(r) {
            if (r.message) {
                frappe.msgprint(__('Nächste Projektnummer wäre: ') + r.message);
            }
        }
    });
}

function zaehler_zuruecksetzen(frm) {
    frappe.prompt([
        {
            label: 'Neue Startnummer',
            fieldname: 'neue_nummer',
            fieldtype: 'Int',
            reqd: 1,
            default: 1
        }
    ], function(values) {
        frm.set_value('aktuelle_nummer', values.neue_nummer);
        frm.save();
    }, __('Zähler zurücksetzen'), __('Zurücksetzen'));
}
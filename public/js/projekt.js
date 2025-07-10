// Custom JavaScript für Project DocType
frappe.ui.form.on('Project', {
    refresh: function(frm) {
        // Custom Styling oder zusätzliche Funktionalität
        setup_naming_series_field(frm);
    },
    
    proj_ns_choice: function(frm) {
        handle_naming_series_change(frm);
    },
    
    custom_project_id: function(frm) {
        if (frm.doc.proj_ns_choice === 'manual' && frm.doc.custom_project_id) {
            validiere_manuellen_projekt_name(frm);
        }
    }
});

function setup_naming_series_field(frm) {
    // Verfügbare Serien für die Dropdown-Liste holen
    frappe.call({
        method: 'custom_logic.custom_logic.doctype.projekt_namensserie.projekt_namensserie.get_available_series',
        callback: function(r) {
            if (r.message) {
                const optionen = r.message.map(serie => ({
                    value: serie.series_name,
                    label: serie.series_label
                }));
                
                // Manuelle Option hinzufügen
                optionen.push({
                    value: 'manual',
                    label: 'Manuelle Eingabe'
                });
                
                // Feld-Optionen aktualisieren
                frm.set_df_property('proj_ns_choice', 'options', 
                    optionen.map(opt => opt.value + '\n' + opt.label).join('\n'));
            }
        }
    });
}

function handle_naming_series_change(frm) {
    if (frm.doc.proj_ns_choice === 'manual') {
        // Manuelle Eingabe Feld zeigen
        frm.set_df_property('custom_project_id', 'hidden', 0);
        frm.set_df_property('custom_project_id', 'reqd', 1);
        frm.set_df_property('custom_project_id', 'read_only', 0);
    } else if (frm.doc.proj_ns_choice) {
        // Manuelle Eingabe verstecken und automatischen Namen generieren
        frm.set_df_property('custom_project_id', 'hidden', 1);
        frm.set_df_property('custom_project_id', 'reqd', 0);
        frm.set_df_property('custom_project_id', 'read_only', 1);
        
        // Vorschau der nächsten Nummer generieren
        frappe.call({
            method: 'custom_logic.custom_logic.doctype.projekt_namensserie.projekt_namensserie.get_next_project_name',
            args: {
                series_name: frm.doc.proj_ns_choice
            },
            callback: function(r) {
                if (r.message && frm.is_new()) {
                    frm.set_value('custom_project_id', r.message);
                    frappe.show_alert({
                        message: __('Nächste Projekt-ID wird sein: ') + r.message,
                        indicator: 'blue'
                    });
                }
            }
        });
    }
}

function validiere_manuellen_projekt_name(frm) {
    if (!frm.doc.custom_project_id) return;
    
    frappe.call({
        method: 'custom_logic.custom_logic.doctype.projekt_namensserie.projekt_namensserie.validate_manual_name',
        args: {
            projekt_name: frm.doc.custom_project_id
        },
        callback: function(r) {
            if (r.message) {
                if (r.message.valid) {
                    frm.set_df_property('custom_project_id', 'description', 
                        '<span style="color: green;">✓ ' + r.message.message + '</span>');
                } else {
                    frm.set_df_property('custom_project_id', 'description', 
                        '<span style="color: red;">✗ ' + r.message.message + '</span>');
                }
            }
        }
    });
}
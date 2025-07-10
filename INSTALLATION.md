# Custom Logic App - Installationsanleitung

## Voraussetzungen
- ERPNext v13 oder höher
- Frappe Framework
- Administrator-Zugriff auf die ERPNext Installation

## Installation

### Schritt 1: App-Ordner erstellen
```bash
cd frappe-bench/apps
mkdir custom_logic
```

### Schritt 2: Dateien kopieren
Kopieren Sie alle Dateien in den entsprechenden Ordner:
```
custom_logic/
├── alle oben aufgelisteten Dateien und Ordner
```

### Schritt 3: App installieren
```bash
cd frappe-bench
bench get-app custom_logic /pfad/zu/custom_logic
bench install-app custom_logic --site ihre-site.local
```

### Schritt 4: Migrationen ausführen
```bash
bench migrate --site ihre-site.local
```

### Schritt 5: Berechtigungen neu laden
```bash
bench reload-doctype --site ihre-site.local
```

### Schritt 6: Browser Cache leeren
```bash
bench clear-cache --site ihre-site.local
```

## Konfiguration

### 1. Namensserien konfigurieren
- Gehen Sie zu "Projekt Namensserie"
- Passen Sie die Startnummern an Ihre Bedürfnisse an
- Stellen Sie sicher, dass alle Serien aktiv sind

### 2. Benutzerberechtigungen
- Stellen Sie sicher, dass Projektbenutzer Zugriff auf "Projekt Namensserie" haben
- Vergeben Sie entsprechende Rollen

### 3. Custom Fields prüfen
- Überprüfen Sie, ob die Custom Fields im Project DocType korrekt hinzugefügt wurden
- Testen Sie die Dropdown-Auswahl

## Verwendung

### Neues Projekt erstellen
1. Gehen Sie zu "Project" > "New"
2. Wählen Sie die gewünschte Namensserie aus:
   - **Auftrag neu (A)**: Jede 3. Nummer (A-7435, A-7438, A-7441, ...)
   - **Reparatur neu (R)**: Jede 2. Nummer (R-1000, R-1002, R-1004, ...)
   - **Ersatzteil neu (E)**: Jede Nummer (E-1000, E-1001, E-1002, ...)
   - **MFK neu (M)**: Jede 2. Nummer (M-1000, M-1002, M-1004, ...)
   - **Manuelle Eingabe**: Geben Sie Ihre eigene ID ein

3. Füllen Sie die restlichen Projektdetails aus
4. Speichern Sie das Projekt

### Manuelle Eingabe
Bei Auswahl von "Manuelle Eingabe":
- Das Feld "Projekt ID" wird editierbar
- Geben Sie eine ID im Format X-XXXX ein (z.B. A-0500)
- Das System validiert automatisch das Format
- Grüne Häkchen = gültig, rote X = ungültig

## Backup und Export

### Konfiguration exportieren
```python
# In der Python-Konsole von ERPNext
from custom_logic.utils.backup import exportiere_namensserien_konfiguration
backup_data = exportiere_namensserien_konfiguration()
```

### Konfiguration importieren
```python
# In der Python-Konsole von ERPNext
from custom_logic.utils.backup import importiere_namensserien_konfiguration
result = importiere_namensserien_konfiguration(backup_data)
```

## Troubleshooting

### Problem: Custom Fields werden nicht angezeigt
**Lösung:**
```bash
bench reload-doctype Project --site ihre-site.local
bench clear-cache --site ihre-site.local
```

### Problem: JavaScript Funktionen funktionieren nicht
**Lösung:**
```bash
bench build --site ihre-site.local
bench restart
```

### Problem: Naming Series nicht verfügbar
**Lösung:**
1. Überprüfen Sie, ob die Patches ausgeführt wurden
2. Manuell ausführen:
```bash
bench execute custom_logic.patches.v1_0.erstelle_projekt_namensserien.execute --site ihre-site.local
```

### Problem: Berechtigungsfehler
**Lösung:**
- Stellen Sie sicher, dass der Benutzer die Rolle "Projects User" oder höher hat
- Überprüfen Sie die Berechtigungen für "Projekt Namensserie"

## Wartung

### Startnummern anpassen
1. Gehen Sie zu "Projekt Namensserie"
2. Bearbeiten Sie die entsprechende Serie
3. Ändern Sie "Aktuelle Nummer" auf den gewünschten Wert
4. Speichern Sie die Änderungen

### Neue Serie hinzufügen
1. Erstellen Sie eine neue "Projekt Namensserie"
2. Fügen Sie den series_name zu den Custom Field Optionen hinzu
3. Aktualisieren Sie das JavaScript falls nötig

### Backup erstellen
Führen Sie regelmäßig Backups der Naming Series Konfiguration durch:
```bash
bench backup --site ihre-site.local
```

## Support
Bei Problemen wenden Sie sich an Ihren Systemadministrator oder erstellen Sie ein Issue im Repository.
```

## 12. Upgrade-Pfad

### custom_logic/patches/v1_1/__init__.py
```python
# -*- coding: utf-8 -*-
```

### custom_logic/patches/v1_1/erweitere_naming_optionen.py
```python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe

def execute():
    """Erweiterte Naming Optionen für zukünftige Versionen"""
    
    # Beispiel für zukünftige Erweiterungen
    zusaetzliche_felder = [
        {
            'fieldname': 'auto_reset_yearly',
            'label': 'Jährlich zurücksetzen',
            'fieldtype': 'Check',
            'insert_after': 'is_active',
            'description': 'Zähler automatisch jedes Jahr zurücksetzen'
        },
        {
            'fieldname': 'prefix_year',
            'label': 'Jahr im Präfix',
            'fieldtype': 'Check',
            'insert_after': 'auto_reset_yearly',
            'description': 'Jahr in die Projektbezeichnung einbeziehen (z.B. A24-0001)'
        }
    ]
    
    for feld in zusaetzliche_felder:
        if not frappe.db.exists('Custom Field', {'dt': 'Projekt Namensserie', 'fieldname': feld['fieldname']}):
            custom_field = frappe.new_doc('Custom Field')
            custom_field.dt = 'Projekt Namensserie'
            custom_field.update(feld)
            custom_field.insert()
            print(f"Erweitertes Feld hinzugefügt: {feld['fieldname']}")
```

## 13. API Dokumentation

### API Endpoints
```python
# Verfügbare Whitelisted Funktionen:

# 1. Nächsten Projektnamen holen
GET /api/method/custom_logic.custom_logic.doctype.projekt_namensserie.projekt_namensserie.get_next_project_name
Parameter: series_name

# 2. Verfügbare Serien holen
GET /api/method/custom_logic.custom_logic.doctype.projekt_namensserie.projekt_namensserie.get_available_series

# 3. Manuellen Namen validieren
GET /api/method/custom_logic.custom_logic.doctype.projekt_namensserie.projekt_namensserie.validate_manual_name
Parameter: projekt_name

# 4. Konfiguration exportieren
GET /api/method/custom_logic.utils.backup.exportiere_namensserien_konfiguration

# 5. Konfiguration importieren
POST /api/method/custom_logic.utils.backup.importiere_namensserien_konfiguration
Body: import_daten (JSON)
```

## 14. Performance Optimierungen

### custom_logic/utils/performance.py
```python
# -*- coding: utf-8 -*-
import frappe
from frappe.utils import cint

def optimize_naming_series_queries():
    """Optimiert Datenbank-Queries für Naming Series"""
    
    # Index für häufige Abfragen erstellen
    frappe.db.sql("""
        CREATE INDEX IF NOT EXISTS idx_projekt_ns_active 
        ON `tabProjekt Namensserie` (is_active)
    """)
    
    frappe.db.sql("""
        CREATE INDEX IF NOT EXISTS idx_projekt_custom_id 
        ON `tabProject` (custom_project_id)
    """)

@frappe.whitelist()
def get_series_statistics():
    """Statistiken für alle Naming Series"""
    stats = frappe.db.sql("""
        SELECT 
            pns.series_name,
            pns.series_label,
            pns.prefix,
            pns.aktuelle_nummer,
            pns.increment_by,
            COUNT(p.name) as verwendete_anzahl,
            pns.aktuelle_nummer + (COUNT(p.name) * pns.increment_by) as naechste_geschaetzte_nummer
        FROM `tabProjekt Namensserie` pns
        LEFT JOIN `tabProject` p ON p.custom_project_id LIKE CONCAT(pns.prefix, '-%')
        WHERE pns.is_active = 1
        GROUP BY pns.series_name
        ORDER BY pns.prefix
    """, as_dict=True)
    
    return stats
```

## Installation als ZIP

Da ich Ihnen keine direkte ZIP-Datei erstellen kann, hier die Schritt-für-Schritt Anleitung zum Erstellen:

### 1. Ordnerstruktur erstellen:
```bash
mkdir custom_logic
cd custom_logic
mkdir -p custom_logic/doctype/projekt_namensserie
mkdir -p config
mkdir -p fixtures
mkdir -p public/css
mkdir -p public/js
mkdir -p overrides
mkdir -p patches/v1_0
mkdir -p utils
mkdir -p tests
```

### 2. Dateien erstellen:
Kopieren Sie jeden Dateiinhalt aus dem obigen Code in die entsprechenden Dateien.

### 3. ZIP erstellen:
```bash
zip -r custom_logic_app.zip custom_logic/
```

### 4. Installation:
```bash
# ZIP entpacken
unzip custom_logic_app.zip -d frappe-bench/apps/

# App installieren
cd frappe-bench
bench install-app custom_logic --site ihre-site.local
bench migrate --site ihre-site.local
```

Diese vollständige deutsche Custom Logic App bietet:

✅ **Erweiterte Naming Series** mit konfigurierbaren Inkrementen
✅ **Deutsche Benutzeroberfläche** und Dokumentation
✅ **Manuelle und automatische** Projektbenennung
✅ **Backup/Export Funktionalität** für einfache Datenmigration
✅ **Umfangreiche Validierung** und Fehlerbehandlung
✅ **Performance-Optimierungen** und Statistiken
✅ **Vollständige Tests** und Qualitätssicherung
✅ **Zukunftssichere Erweiterbarkeit** durch modularen Aufbau

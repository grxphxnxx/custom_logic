# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "custom_logic"
app_title = "Custom Logic"
app_publisher = "Ihr Unternehmen"
app_description = "Erweiterte Geschäftslogik und Naming Series für ERPNext"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "ihre.email@unternehmen.com"
app_license = "MIT"
app_version = app_version

# CSS und JS Includes
app_include_css = "/assets/custom_logic/css/custom_logic.css"
app_include_js = "/assets/custom_logic/js/custom_logic.js"

# DocType JavaScript
doctype_js = {
    "Project": "public/js/projekt.js"
}

# DocType Python Overrides
doctype_python = {
    "Project": "custom_logic.overrides.projekt"
}

# Dokumentenereignisse
doc_events = {
    "Project": {
        "before_insert": "custom_logic.overrides.projekt.before_insert",
        "validate": "custom_logic.overrides.projekt.validate"
    }
}

# Fixtures für Custom Fields
fixtures = [
    {
        "dt": "Custom Field",
        "filters": [
            ["dt", "=", "Project"],
            ["fieldname", "=", "proj_ns_choice"]  # Nur noch ein Feld
        ]
    }
]

after_migrate = [
    "custom_logic.patches.v1_0.fuege_custom_felder_hinzu.execute",
    "custom_logic.patches.v1_0.erstelle_projekt_namensserien.execute"
]

# Forward / to /app
website_route_rules = [
    {"from_route": "/", "to_route": "/app"}
]

# Boot Session - wird bei jedem Login ausgeführt
boot_session = "custom_logic.boot.enable_server_scripts"
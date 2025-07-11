# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version


app_name = "custom_logic"
app_title = "Custom Logic"
app_publisher = "Ihr Unternehmen"
app_description = "Server Scripts Aktivierung"
app_version = "1.0.0"

# Boot Session - Server Scripts aktivieren
boot_session = "custom_logic.boot.enable_server_scripts"
# Forward / to /app
website_route_rules = [
    {"from_route": "/", "to_route": "/app"}
]

# Boot Session - wird bei jedem Login ausgeführt
boot_session = "custom_logic.boot.enable_server_scripts"
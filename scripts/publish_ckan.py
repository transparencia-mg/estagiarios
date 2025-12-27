#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import sys

CKAN_HOST = os.getenv("CKAN_HOST")
CKAN_KEY = os.getenv("CKAN_KEY")

if not CKAN_HOST or not CKAN_KEY:
    print("❌ CKAN_HOST ou CKAN_KEY não definidos")
    sys.exit(1)

print("🚀 Publicando / atualizando dataset no CKAN com DataStore...")

cmd = [
    "dpckan",
    "--ckan-host", CKAN_HOST,
    "--ckan-key", CKAN_KEY,
    "--datastore",
    "--datapackage", "datapackage/datapackage.json",
    "dataset", "update"
]

subprocess.run(cmd, check=True)

print("✅ Publicação concluída com sucesso")

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

base_cmd = [
    "dpckan",
    "--ckan-host", CKAN_HOST,
    "--ckan-key", CKAN_KEY,
    "--datastore",
    "--datapackage", "datapackage/datapackage.json"
]

print("🔄 Tentando atualizar dataset no CKAN...")
update_cmd = base_cmd + ["dataset", "update"]

result = subprocess.run(update_cmd)

if result.returncode != 0:
    print("ℹ Dataset não existe. Criando dataset...")
    create_cmd = base_cmd + ["dataset", "create"]
    subprocess.run(create_cmd, check=True)
else:
    print("✅ Dataset atualizado com sucesso")

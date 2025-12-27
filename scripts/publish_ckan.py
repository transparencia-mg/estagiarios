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
result = subprocess.run(
    base_cmd + ["dataset", "update"],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print("⚠️ Falha ao atualizar dataset")
    print(result.stdout)
    print(result.stderr)

    print("🆕 Tentando criar dataset...")
    subprocess.run(
        base_cmd + ["dataset", "create"],
        check=True
    )
else:
    print("✅ Dataset atualizado com sucesso")


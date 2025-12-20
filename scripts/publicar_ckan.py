#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import requests
from pathlib import Path

CKAN_URL = "https://www.dados.mg.gov.br"
API_KEY = os.environ.get("CKAN_KEY")

if not API_KEY:
    raise RuntimeError("CKAN_KEY não definida")

HEADERS = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

DATAPACKAGE = Path("datapackage/datapackage.json")
if not DATAPACKAGE.exists():
    raise RuntimeError("datapackage.json não encontrado")

dp = json.loads(DATAPACKAGE.read_text(encoding="utf-8"))

DATASET_NAME = dp["name"]
OWNER_ORG = dp["owner_org"]

# =========================
# Verifica se dataset existe
# =========================
resp = requests.get(
    f"{CKAN_URL}/api/3/action/package_show",
    params={"id": DATASET_NAME},
    headers=HEADERS
)

exists = resp.status_code == 200

payload = {
    "name": DATASET_NAME,
    "title": dp["title"],
    "notes": dp["description"],
    "owner_org": OWNER_ORG,
    "private": False
}

# =========================
# Create ou Update dataset
# =========================
if exists:
    print("🔄 Atualizando dataset no CKAN...")
    url = f"{CKAN_URL}/api/3/action/package_update"
else:
    print("🆕 Criando dataset no CKAN...")
    url = f"{CKAN_URL}/api/3/action/package_create"

r = requests.post(url, headers=HEADERS, json=payload)
r.raise_for_status()

dataset = r.json()["result"]
dataset_id = dataset["id"]

# =====





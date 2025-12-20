#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import requests
from pathlib import Path

# =============================
# CONFIGURAÇÕES
# =============================
CKAN_URL = "https://www.dados.mg.gov.br"
API_KEY = os.environ.get("CKAN_KEY")

if not API_KEY:
    raise RuntimeError("CKAN_KEY não encontrada como variável de ambiente")

HEADERS = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

DATASET_NAME = "estagiarios-governo-minas-gerais"
OWNER_ORG = "controladoria-geral-do-estado-cge"
GITHUB_REPO = "transparencia-mg/estagiarios"
GITHUB_BRANCH = "main"

# =============================
# Carregar datapackage
# =============================
datapackage = json.loads(
    Path("datapackage/datapackage.json").read_text(encoding="utf-8")
)

# =============================
# Criar ou atualizar dataset
# =============================
dataset_payload = {
    "name": DATASET_NAME,
    "title": datapackage["title"],
    "notes": datapackage["description"],
    "owner_org": OWNER_ORG,
    "license_id": "cc-by",
    "state": "active"
}

# Verifica se o dataset já existe
r = requests.post(
    f"{CKAN_URL}/api/3/action/package_show",
    headers=HEADERS,
    json={"id": DATASET_NAME}
)

action = "package_update" if r.ok else "package_create"

r = requests.post(
    f"{CKAN_URL}/api/3/action/{action}",
    headers=HEADERS,
    json=dataset_payload
)

if not r.ok:
    raise RuntimeError(f"Erro ao criar/atualizar dataset: {r.text}")

print("✔ Dataset publicado/atualizado com sucesso.")

# =============================
# Criar / atualizar recursos
# =============================
for res in datapackage["resources"]:
    resource_url = (
        f"https://raw.githubusercontent.com/"
        f"{GITHUB_REPO}/{GITHUB_BRANCH}/{res['path']}"
    )

    resource_payload = {
        "package_id": DATASET_NAME,
        "name": res["name"],
        "url": resource_url,
        "format": "CSV",
        "description": res["description"],
        "schema": res.get("schema")
    }

    # Verifica se o recurso já existe
    r = requests.post(
        f"{CKAN_URL}/api/3/action/resource_search",
        headers=HEADERS,
        json={
            "query": f"name:{res['name']}",
            "package_id": DATASET_NAME
        }
    )

    exists = r.ok and r.json()["result"]["count"] > 0

    if exists:
        resource_id = r.json()["result"]["results"][0]["id"]
        resource_payload["id"] = resource_id
        action = "resource_update"
    else:
        action = "resource_create"

    r = requests.post(
        f"{CKAN_URL}/api/3/action/{action}",
        headers=HEADERS,
        json=resource_payload
    )

    if r.ok:
        print(f"✔ Recurso publicado: {res['title']}")
    else:
        print(f"⚠ Erro ao publicar recurso {res['title']}: {r.text}")

print("🏁 Publicação no CKAN finalizada.")




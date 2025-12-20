#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import hashlib
from pathlib import Path

# =========================
# CONFIGURAÇÕES
# =========================
DATA_DIR = Path("data")
OUTPUT = Path("datapackage/datapackage.json")

# =========================
# FUNÇÃO HASH
# =========================
def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

# =========================
# SCHEMA
# =========================
SCHEMA_FIELDS = [
    {"name": "ano_mesreferencia", "type": "string"},
    {"name": "nome_estagiario", "type": "string"},
    {"name": "masp", "type": "string"},
    {"name": "codigo_situacao_funcional", "type": "string"},
    {"name": "situacao_funcional", "type": "string"},
    {"name": "data_inicio", "type": "string"},
    {"name": "data_fim", "type": "string"},
    {"name": "codigo_orgao", "type": "string"},
    {"name": "orgao", "type": "string"},
    {"name": "sigla_orgao", "type": "string"},
    {"name": "valor_remuneracao", "type": "string"}
]

# =========================
# COLETA DOS CSVs (ROBUSTA)
# =========================
csv_files = sorted(DATA_DIR.glob("*.csv"))

if not csv_files:
    raise RuntimeError("Nenhum arquivo CSV encontrado na pasta data/")

resources = []

for csv in csv_files:
    nome = csv.stem.replace("_", "-")
    checksum = file_hash(csv)

    resources.append({
        "name": nome.lower(),
        "title": f"Estagiários do Governo de Minas Gerais – {csv.stem}",
        "path": f"data/{csv.name}",
        "format": "csv",
        "mediatype": "text/csv",
        "encoding": "utf-8",
        "hash": checksum,
        "schema": {
            "fields": SCHEMA_FIELDS
        }
    })

# =========================
# DATAPACKAGE
# =========================
datapackage = {
    "profile": "data-package",
    "name": "estagiarios-governo-minas-gerais",
    "title": "Estagiários do Governo do Estado de Minas Gerais",
    "description": "Dados cadastrais e de remuneração dos estagiários do Governo de Minas Gerais.",
    "owner_org": "controladoria-geral-do-estado-cge",
    "ckan": {
        "owner_org": "controladoria-geral-do-estado-cge",
        "private": False,
        "state": "active"
    },
    "license": {
        "type": "CC-BY-4.0",
        "title": "Creative Commons Attribution 4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/"
    },
    "resources": resources
}

# =========================
# ESCRITA
# =========================
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(
    json.dumps(datapackage, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print("✅ datapackage.json gerado com sucesso")


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import hashlib
from pathlib import Path
from gerar_schema import gerar_schema

BASE_DIR = Path(".")
DATA_DIR = BASE_DIR / "data"
OUTPUT = BASE_DIR / "datapackage" / "datapackage.json"

resources = []

for csv in sorted(DATA_DIR.glob("estagiarios_*.csv")):
    ano = csv.stem.split("_")[-1]

    hash_md5 = hashlib.md5(csv.read_bytes()).hexdigest()

    schema = gerar_schema(csv)

    resources.append({
        "name": f"estagiarios-{ano}",
        "title": f"Estagiários do Governo de Minas Gerais – {ano}",
        "path": f"data/{csv.name}",
        "format": "csv",
        "mediatype": "text/csv",
        "encoding": "latin1",
        "hash": f"md5:{hash_md5}",
        "schema": schema
    })

datapackage = {
    "profile": "tabular-data-package",
    "name": "estagiarios-governo-minas-gerais",
    "title": "Estagiários do Governo do Estado de Minas Gerais",
    "description": (
        "Relação de estagiários vinculados aos órgãos e entidades "
        "do Poder Executivo do Estado de Minas Gerais."
    ),
    "keywords": [
        "estagiários",
        "educação",
        "recursos humanos",
        "Governo de Minas Gerais"
    ],
    "license": "CC-BY-4.0",
    "sources": [
        {
            "title": "Portal da Transparência do Estado de Minas Gerais",
            "path": "https://www.transparencia.mg.gov.br"
        }
    ],
    "resources": resources
}

OUTPUT.parent.mkdir(exist_ok=True)
OUTPUT.write_text(
    json.dumps(datapackage, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("✔ datapackage.json gerado com encoding tolerante, hash e schema")



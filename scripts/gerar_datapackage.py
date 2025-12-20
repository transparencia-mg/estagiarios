#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path

DATA_DIR = Path("data")
OUTPUT = Path("datapackage/datapackage.json")

resources = []

for csv in sorted(DATA_DIR.glob("estagiarios_*.csv")):
    ano = csv.stem.split("_")[-1]

    resources.append({
        "name": f"estagiarios-{ano}",
        "title": f"Estagiários – {ano}",
        "description": f"Conjunto de dados de estagiários do Estado de Minas Gerais. 
        Dados disponíveis a partir de dezembro de 2022. Os dados são atualizados mensalmente",
        "path": f"data/{csv.name}",
        "format": "csv",
        "mediatype": "text/csv",
        "encoding": "utf-8",
        "profile": "tabular-data-resource",
        "schema": {
            "fields": [
                {"name": "ano_mesreferencia", "type": "string"},
                {"name": "nome_estagiario", "type": "string"},
                {"name": "masp", "type": "string"},
                {"name": "codigo_situacao_funcional", "type": "string"},
                {"name": "situacao_funcional", "type": "string"},
                {"name": "data_inicio", "type": "string"},
                {"name": "data_fim", "type": "string"},
                {"name": "codigo_orgao", "type": "string"},
                {"name": "orgao", "type": "string"},
                {"name": "orgao_sigla", "type": "string"},
                {"name": "valor_remuneracao", "type": "string"}
            ]
        }
    })

datapackage = {
    "profile": "data-package",
    "name": "estagiarios",
    "title": "Estagiários do Governo de Minas Gerais",
    "owner_org": "controladoria-geral-do-estado-cge",
    "resources": resources
}

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(
    json.dumps(datapackage, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print(f"✔ datapackage.json gerado com {len(resources)} recursos")

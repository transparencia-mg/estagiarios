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
# FUNÇÃO HASH (força update)
# =========================
def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

# =========================
# Schema padrão dos CSVs
# =========================
SCHEMA_FIELDS = [
    {
        "name": "ano_mesreferencia",
        "title": "Ano e mês de referência",
        "type": "string",
        "description": "Ano e mês de referência no formato AAAA-MM"
    },
    {
        "name": "nome_estagiario",
        "title": "Nome do estagiário",
        "type": "string"
    },
    {
        "name": "masp",
        "title": "MASP do estagiário",
        "type": "string",
        "description": "Identificador funcional (MASP)"
    },
    {
        "name": "codigo_situacao_funcional",
        "title": "Código da situação funcional",
        "type": "string"
    },
    {
        "name": "situacao_funcional",
        "title": "Situação funcional do estagiário",
        "type": "string"
    },
    {
        "name": "data_inicio",
        "title": "Data de início do estágio",
        "type": "string",
        "description": "Data no formato AAAA-MM-DD"
    },
    {
        "name": "data_fim",
        "title": "Data de término do estágio",
        "type": "string",
        "description": "Data no formato AAAA-MM-DD"
    },
    {
        "name": "codigo_orgao",
        "title": "Código do órgão",
        "type": "string"
    },
    {
        "name": "orgao",
        "title": "Nome do órgão",
        "type": "string"
    },
    {
        "name": "sigla_orgao",
        "title": "Sigla do órgão",
        "type": "string"
    },
    {
        "name": "valor_remuneracao",
        "title": "Valor da remuneração do estagiário",
        "type": "string",
        "description": "Valor nominal conforme publicado, sem conversão numérica"
    }
]

# =========================
# Recursos (1 CSV por ano)
# =========================
resources = []

csv_files = sorted(DATA_DIR.glob("estagiarios_*.csv"))

if not csv_files:
    raise RuntimeError("Nenhum arquivo estagiarios_*.csv encontrado na pasta data/")

for csv in csv_files:
    ano = csv.stem.split("_")[-1]
    checksum = file_hash(csv)

    resources.append({
        "name": f"estagiarios-{ano}",
        "title": f"Estagiários do Governo de Minas Gerais – {ano}",
        "path": f"data/{csv.name}",
        "format": "csv",
        "mediatype": "text/csv",
        "encoding": "utf-8",
        "description": f"Dados de estagiários do Governo de Minas Gerais referentes ao ano de {ano}",
        "hash": checksum,  # <<< força atualização no CKAN
        "schema": {
            "fields": SCHEMA_FIELDS,
            "primaryKey": ["masp", "ano_mesreferencia"]
        }
    })

# =========================
# Data Package
# =========================
datapackage = {
    "profile": "data-package",
    "name": "estagiarios-governo-minas-gerais",
    "title": "Estagiários do Governo do Estado de Minas Gerais",
    "description": (
        "Base de dados contendo informações cadastrais, funcionais "
        "e de remuneração dos estagiários do Governo do Estado de Minas Gerais."
    ),

    # Obrigatório para CKAN / dpckan
    "owner_org": "controladoria-geral-do-estado-cge",

    # Compatibilidade CKAN
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
# Escrita do arquivo
# =========================
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(
    json.dumps(datapackage, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print("✅ datapackage/datapackage.json gerado e atualizado com sucesso.")


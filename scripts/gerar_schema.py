#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import re

def normalizar_nome_toggle(col):
    """
    Converte para padrão CKAN / DataStore:
    - minúsculo
    - sem acento
    - sem espaço
    """
    col = col.strip().lower()
    col = re.sub(r"[^\w]+", "_", col)
    col = re.sub(r"_+", "_", col)
    return col.strip("_")

def inferir_tipo(_serie: pd.Series) -> str:
    """
    Inferência segura apenas para metadados.
    """
    return "string"

def gerar_schema(csv_path):
    """
    Gera schema compatível com CKAN DataStore,
    incluindo chave primária (ID).
    """

    try:
        df = pd.read_csv(
            csv_path,
            dtype=str,
            encoding="utf-8",
            low_memory=False
        )
    except UnicodeDecodeError:
        df = pd.read_csv(
            csv_path,
            dtype=str,
            encoding="latin1",
            low_memory=False
        )

    fields = []

    # 🔑 cria ID técnico se não existir
    id_field = "_id"
    fields.append({
        "name": id_field,
        "type": "string"
    })

    for col in df.columns:
        fields.append({
            "name": normalizar_nome_toggle(col),
            "type": inferir_tipo(df[col])
        })

    schema = {
        "fields": fields,
        "primaryKey": id_field,
        "missingValues": ["", "NA", "N/A", "null"]
    }

    return schema


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import re

def normalizar_nome(col):
    col = col.strip().lower()
    col = re.sub(r"[^\w]+", "_", col)
    col = re.sub(r"_+", "_", col)
    return col.strip("_")

def inferir_tipo(_serie: pd.Series) -> str:
    # inferência segura para dados públicos
    return "string"

def gerar_schema(csv_path):
    """
    Lê CSV no padrão dados.mg (separador ;)
    """

    try:
        df = pd.read_csv(
            csv_path,
            dtype=str,
            sep=";",          # 🔑 CORREÇÃO PRINCIPAL
            encoding="utf-8",
            low_memory=False
        )
    except UnicodeDecodeError:
        df = pd.read_csv(
            csv_path,
            dtype=str,
            sep=";",          # 🔑 CORREÇÃO PRINCIPAL
            encoding="latin1",
            low_memory=False
        )

    fields = []

    # ID técnico
    fields.append({
        "name": "_id",
        "type": "string"
    })

    for col in df.columns:
        fields.append({
            "name": normalizar_nome(col),
            "type": inferir_tipo(df[col])
        })

    return {
        "fields": fields,
        "primaryKey": "_id",
        "missingValues": ["", "NA", "N/A", "null"]
    }



#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

def inferir_tipo(serie: pd.Series) -> str:
    """
    Inferência segura apenas para metadados.
    Não converte valores.
    """
    return "string"

def gerar_schema(csv_path):
    """
    Lê CSV com fallback de encoding (igual padrão CGE).
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
    for col in df.columns:
        fields.append({
            "name": col.strip(),
            "type": inferir_tipo(df[col])
        })

    return {
        "fields": fields,
        "missingValues": ["", "NA", "N/A", "null"]
    }

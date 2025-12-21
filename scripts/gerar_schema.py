#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

def inferir_tipo(serie: pd.Series) -> str:
    if pd.api.types.is_integer_dtype(serie):
        return "integer"
    if pd.api.types.is_float_dtype(serie):
        return "number"
    if pd.api.types.is_datetime64_any_dtype(serie):
        return "date"
    return "string"

def gerar_schema(csv_path):
    df = pd.read_csv(csv_path, dtype=str)

    fields = []
    for col in df.columns:
        fields.append({
            "name": col,
            "type": inferir_tipo(df[col])
        })

    return {
        "fields": fields,
        "missingValues": ["", "NA", "N/A", "null"]
    }


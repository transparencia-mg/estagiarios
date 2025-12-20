#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
normalizar_ano_mesreferencia.py

Converte a coluna 'ano_mesreferencia' do formato:
AAAA/MM  →  MM/AAAA

Regras:
- NÃO altera outras colunas
- NÃO converte tipos
- Mantém células vazias vazias
- Atualiza os arquivos CSV na pasta /data
"""

from pathlib import Path
import pandas as pd

# =========================
# CONFIGURAÇÕES
# =========================
DATA_DIR = Path("data")
COLUNA_DATA = "ano_mesreferencia"

# =========================
# FUNÇÃO DE CONVERSÃO
# =========================
def converter_ano_mes(valor: str) -> str:
    if not valor or not isinstance(valor, str):
        return ""
    partes = valor.split("/")
    if len(partes) == 2:
        # AAAA/MM → MM/AAAA
        return f"{partes[1]}/{partes[0]}"
    return valor

# =========================
# PROCESSAMENTO
# =========================
def main():
    if not DATA_DIR.exists():
        raise FileNotFoundError("Pasta /data não encontrada")

    arquivos = sorted(DATA_DIR.glob("*.csv"))

    if not arquivos:
        print("Nenhum CSV encontrado para processar")
        return

    for arquivo in arquivos:
        print(f"Processando: {arquivo.name}")

        df = pd.read_csv(
            arquivo,
            dtype=str,
            keep_default_na=False,
            encoding="utf-8"
        )

        if COLUNA_DATA not in df.columns:
            print(f"  ⚠ Coluna '{COLUNA_DATA}' não encontrada — ignorado")
            continue

        df[COLUNA_DATA] = df[COLUNA_DATA].apply(converter_ano_mes)

        df.to_csv(
            arquivo,
            index=False,
            encoding="utf-8"
        )

        print("  ✔ Normalizado com sucesso")

if __name__ == "__main__":
    main()

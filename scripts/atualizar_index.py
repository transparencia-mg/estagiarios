#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

INDEX = Path("index.html")

inicio = "<!-- INICIO_DADOS_AUTOMATICOS -->"
fim = "<!-- FIM_DADOS_AUTOMATICOS -->"

novo = """
<script>
console.log("Bloco atualizado automaticamente");
</script>
""".strip()

html = INDEX.read_text(encoding="utf-8")

# ===============================
# VALIDAÇÃO OBRIGATÓRIA
# ===============================

if inicio not in html:
    raise RuntimeError(
        "ERRO: marcador não encontrado:\n"
        "<!-- INICIO_DADOS_AUTOMATICOS -->"
    )

if fim not in html:
    raise RuntimeError(
        "ERRO: marcador não encontrado:\n"
        "<!-- FIM_DADOS_AUTOMATICOS -->"
    )

if html.index(inicio) > html.index(fim):
    raise RuntimeError(
        "ERRO: marcador INICIO está depois do FIM"
    )

# ===============================
# SUBSTITUIÇÃO SEGURA
# ===============================

antes = html.split(inicio)[0]
depois = html.split(fim)[1]

html_final = (
    antes
    + inicio + "\n"
    + novo + "\n"
    + fim
    + depois
)

INDEX.write_text(html_final, encoding="utf-8")

print("index.html atualizado com sucesso")

Conjunto de dados contendo informações cadastrais, funcionais e de remuneração dos **estagiários vinculados aos órgãos e entidades do Governo do Estado de Minas Gerais**, disponibilizado em conformidade com a política de transparência e dados abertos do Estado.

---

## 📌 Descrição Geral

Esta base de dados reúne informações consolidadas sobre estagiários em exercício no Poder Executivo Estadual, permitindo o acompanhamento público da força de trabalho de estagiários, sua distribuição institucional e evolução ao longo do tempo.

Os dados são organizados em arquivos anuais e seguem um **padrão estruturado**, facilitando o uso por cidadãos, pesquisadores, órgãos de controle e desenvolvedores.

---

## 📊 Conteúdo dos Dados

Os arquivos disponibilizados contêm, entre outros, os seguintes campos:

- `ano_mesreferencia` — Ano e mês de referência da informação
- `nome_estagiario` — Nome do estagiário
- `masp` — Identificador funcional (MASP)
- `codigo_situacao_funcional` — Código da situação funcional
- `situacao_funcional` — Descrição da situação funcional
- `data_inicio` — Data de início do estágio
- `data_fim` — Data de término do estágio
- `codigo_orgao` — Código do órgão de exercício
- `orgao` — Nome do órgão
- `sigla_orgao` — Sigla do órgão
- `valor_remuneracao` — Valor da remuneração do estagiário

---

## 📁 Organização dos Arquivos

- Os dados são disponibilizados em **formato CSV**
- Cada arquivo corresponde a um **ano de referência**
- O conjunto de dados é descrito por um arquivo `datapackage.json`, garantindo interoperabilidade e padronização conforme boas práticas de dados abertos

---

## 🔄 Periodicidade de Atualização

A atualização dos dados ocorre de forma mensal, conforme a disponibilização das informações pelos sistemas corporativos do Estado, com inclusão de novos períodos e eventuais correções quando necessárias.

---

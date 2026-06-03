
SANKHYA_KNOWLEDGE_BASE = {
    "TGFCAB": {
        "description": "Cabeçalho da Nota Fiscal (Compras, Vendas, Requisições). Tabela central.",
        "business_terms": ["nota fiscal", "NF", "venda", "compra", "faturamento"],
        "relations": [
            {
                "table": "TGFPAR",
                "join": "TGFCAB.CODPARC = TGFPAR.CODPARC",
                "meaning": "Parceiro (cliente/fornecedor) da nota"
            },
            {
                "table": "TGFITE",
                "join": "TGFCAB.NUNOTA = TGFITE.NUNOTA",
                "meaning": "Itens da nota fiscal"
            },
            {
                "table": "TGFTOP",
                "join": "TGFCAB.CODTIPOPER = TGFTOP.CODTIPOPER",
                "meaning": "Tipo de operação (natureza da operação)"
            }
        ],
        "key_fields": ["NUNOTA", "NUNNOTA", "DTNEG", "CODPARC", "CODTIPOPER", "STATUSNOTA"]
    },
    "TGFPAR": {
        "description": "Cadastro de Parceiros (Clientes e Fornecedores).",
        "business_terms": ["cliente", "fornecedor", "parceiro", "CPF", "CNPJ"],
        "relations": [
            {
                "table": "TGFCAB",
                "join": "TGFPAR.CODPARC = TGFCAB.CODPARC",
                "meaning": "Notas fiscais do parceiro"
            }
        ],
        "key_fields": ["CODPARC", "NOMEPARC", "CGC", "TIPPARC"]
    },
    "TGFPRO": {
        "description": "Cadastro de Produtos.",
        "business_terms": ["produto", "mercadoria", "item", "SKU"],
        "relations": [
            {
                "table": "TGFITE",
                "join": "TGFPRO.CODPROD = TGFITE.CODPROD",
                "meaning": "Itens de nota que contêm o produto"
            }
        ],
        "key_fields": ["CODPROD", "DESCRPROD", "CODBARRA"]
    },
    # Adicione mais tabelas conforme sua necessidade
}
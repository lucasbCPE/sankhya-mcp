
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
    "AD_CPECADPROMOP": {
        "description": "Formulário de Promoção de Pessoal. Controla as requisições de alteração de cargo, setor, salário e comissão dos colaboradores, além de registrar o fluxo de aprovação pelo Head e Diretoria.",
        "business_terms": [
            "promoção", 
            "reajuste salarial", 
            "mudança de cargo", 
            "alteração de ganhos", 
            "aprovação de head", 
            "aprovação de diretoria",
            "mudança de setor"
        ],
        "relations": [
            {
                "table": "TFPFUN", 
                "join": "AD_CPECADPROMOP.CODFUNC = TFPFUN.CODFUNC",
                "meaning": "Vínculo com o cadastro oficial do funcionário no DP"
            },
            {
                "table": "TWFPRN",
                "join": "AD_CPECADPROMOP.IDINSTPRN = TWFPRN.IDINSTPRN",
                "meaning": "Vínculo com a instância do processo no Sankhya Flow (BPM)"
            }
        ],
        "key_fields": [
            "CODREGISTRO", 
            "IDINSTPRN", 
            "CODFUNC", 
            "COLABORADOR",
            "CARGOATUAL", 
            "CARGOPROP", 
            "SALARIOATUAL", 
            "SALARIOPROP", 
            "STATUS"
        ],
        # Domain values vai "traduzir" dados salvos no banco como letra pra entender o significado das mesmas
        "domain_values": {
            "MOTIVOPROMO": {"D": "Desempenho", "R": "Reajuste salarial"},
            "ALTGANHO": {"S": "Salário", "C": "Comissão", "A": "Ambos"},
            "APROVADOHEAD": {"A": "Aprovado", "R": "Reprovado"},
            "APROVADODIR": {"A": "Aprovado", "R": "Rejeitado"},
            "STATUS": {"F": "Finalizado"},
            "APROVACAO": {"A": "Aprovado", "R": "Reprovado"},
            "SETORATUAL": {
                "1": "Comercial", "2": "Processos", "3": "Estoque", "4": "Compras", "5": "Faturamento",
                "6": "Assistência", "7": "Cadastro", "8": "Cobrança", "9": "Comex", "10": "Controladoria",
                "11": "RH", "12": "Drones", "13": "Suporte", "14": "Licenciados", 
                "15": "Financeiro", "16": "Marketing", "17": "Experiência do Cliente",
                "18": "TI", "19": "Mercado Topográfico", "20": "Fiscal"
            },
            "SETORPROP": {
                "1": "Comercial", "2": "Processos", "3": "Estoque", "4": "Compras", "5": "Faturamento",
                "6": "Assistência", "7": "Cadastro", "8": "Cobrança", "9": "Comex", "10": "Controladoria",
                "11": "RH", "12": "Drones", "13": "Suporte", "14": "Licenciados", 
                "15": "Financeiro", "16": "Marketing", "17": "Experiência do Cliente",
                "18": "TI", "19": "Mercado Topográfico", "20": "Fiscal"
            }
        }
    }
}
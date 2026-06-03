import asyncio
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from sqlalchemy import create_engine, inspect, text

from baseconhecimento import SANKHYA_KNOWLEDGE_BASE

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

def get_engine():
    """Cria uma engine de conexão com o banco de dados usando as variáveis de ambiente."""
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_database = os.getenv("DB_DATABASE")

    connection_string = (
        f"mssql+pymssql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
    )
    return create_engine(connection_string, echo=False)

engine = get_engine()

server = Server("sankhya-mcp")

@server.list_tools()
async def hadle_list_tools() -> list[Tool]:    
    return [
        Tool(
            name="list_tables",
            description="Lista as tabelas disponíveis no banco de dados.",
            inputSchema={
                "type": "object", "properties": {}}
        ),
        Tool(
            name="get_table_info",
            description="Obtém a estrutura de uma tabela, com colunas, chaves estrangeiras e relações de negócio.",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "Nome da tabela para obter informações."}
                },
                "required": ["table_name"]
            }
        ),
        Tool(
            name="search_tables",
            description="Busca tabelas cujo nome ou descrição contenham um termo (ex: 'nota', 'produto').",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Termo para buscar nas tabelas."}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="execute_query",
            description="Executa uma consulta SQL no banco de dados e retorna os resultados.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Consulta SQL a ser executada."}
                },
                "required": ["query"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        if name == "list_tables":
            return await list_tables()
        
        elif name == "get_table_info":
            return await get_table_info(arguments["table_name"])
        
        elif name == "search_tables":
            return await search_tables(arguments["query"])
        
        elif name == "execute_query":
            return await execute_query(arguments["query"])
        
        else:
            return [TextContent(type="text", text=f"Ferramenta desconhecida: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Erro ao executar a ferramenta: {str(e)}")]

async def list_tables():
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        return [TextContent(type="text", text=json.dumps({"tables": tables}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Erro ao listar tabelas: {str(e)}")]

async def get_table_info(table_name: str):
    try:
        inspector = inspect(engine)
        columns = inspector.get_columns(table_name)
        pk = inspector.get_pk_constraint(table_name)
        fks = inspector.get_foreign_keys(table_name)
        knowledge = SANKHYA_KNOWLEDGE_BASE.get(table_name.upper(), {})

        result = {
            "table": table_name,
            "description": knowledge.get("description", "Tabela sem descrição cadastrada."),
            "primary_key": pk,
            "columns": [{"name": c["name"], "type": str(c["type"])} for c in columns],
            "foreign_keys": fks,
            "business_relations": knowledge.get("relations", []),
            "key_fields": knowledge.get("key_fields", []),
            "domain_values": knowledge.get("domain_values", {})
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
    except Exception as e:
        return [TextContent(type="text", text=f"Erro ao obter informações da tabela '{table_name}': {str(e)}")]
    
async def search_tables(query: str):
    try:
        inspector = inspect(engine)
        all_tables = inspector.get_table_names()
        matches = []
        for t in all_tables:
            kn = SANKHYA_KNOWLEDGE_BASE.get(t.upper(), {})
            desc = kn.get("description", "")
            terms = kn.get("business_terms", [])
            if (query.lower() in t.lower() or
                query.lower() in desc.lower() or
                any(query.lower() in term for term in terms)):
                matches.append({
                    "table": t,
                    "description": desc
                })
        return [TextContent(type="text", text=json.dumps(matches, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Erro na busca: {str(e)}")]

async def execute_query(sql: str):
    if not sql.strip().upper().startswith("SELECT"):
        return [TextContent(type="text", text="Erro: Apenas consultas SELECT são permitidas.")]
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            rows = [dict(row._mapping) for row in result.fetchmany(100)] 
            columns = list(rows[0].keys()) if rows else []
            return [TextContent(
                type="text",
                text=json.dumps({
                    "columns": columns,
                    "row_count": len(rows),
                    "rows": rows
                }, indent=2, default=str)
            )]
    except Exception as e:
        return [TextContent(type="text", text=f"Erro na execução da consulta: {str(e)}")]
    
async def run_server():
    # Configura as opções de inicialização de acordo com o padrão mais recente da SDK
    options = InitializationOptions(
        server_name="sankhya-mcp",
        server_version="0.1.0",
        capabilities=server.get_capabilities(
            notification_options=NotificationOptions(),
            experimental_capabilities={},
        )
    )
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            options
        )

if __name__ == "__main__":
    asyncio.run(run_server())
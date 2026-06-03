

# 🚀 Sankhya MCP Server

Este projeto é um servidor Model Context Protocol (MCP) desenvolvido integralmente em Python para interagir de forma inteligente com os sistemas Sankhya, facilitando operações como a exportação de metadados de tabelas.

Este guia é destinado à equipe de TI e descreve o processo de clonagem, configuração no Claude Desktop e o fluxo de versionamento (Git Flow) que utilizamos para garantir a integridade do código e evitar que o trabalho da equipe seja sobrescrito.

---

## 🛠️ 1. Instalação e Configuração do Ambiente

### Pré-requisitos
* **Python 3.10+** instalado
* **Git** instalado
* **Claude Desktop** instalado

### Clonando e Preparando o Repositório

1. **Faça o clone do repositório:**
   ```bash
   git clone [https://github.com/lucasbCPE/sankhya-mcp.git](https://github.com/lucasbCPE/sankhya-mcp.git)
   cd sankhya-mcp


2. **Crie e ative um ambiente virtual (Recomendado):**
* No Windows:
```bash
python -m venv venv
venv\Scripts\activate

```


* No macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate

```




3. **Instale as dependências:**
O projeto lista as dependências no arquivo `requisitos.txt`. Execute:


```bash
pip install -r requisitos.txt

```


4. **Configuração do arquivo `.env`:**
O arquivo `.env` possui informações sensíveis e é devidamente ignorado pelo `.gitignore`. Portanto, ele não vai junto no `git clone`. Você precisará criá-lo manualmente na raiz do repositório com o seguinte formato:


```env
SANKHYA_API_URL=[https://api.sankhya.suaempresa.com.br](https://api.sankhya.suaempresa.com.br)
SANKHYA_USER=seu_usuario
SANKHYA_PASSWORD=sua_senha
# Solicite as credenciais de homologação/desenvolvimento ao administrador do sistema.

```



---

## 🤖 2. Integrando ao Claude Desktop

Para que o Claude Desktop reconheça o servidor `server.py`  e passe a ter acesso às ferramentas do Sankhya, é necessário alterar o arquivo de configuração do aplicativo.

1. **Localize e abra o arquivo de configuração do Claude Desktop:**
* **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
* **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
* **Ou entre no Claude desktop vá até `configurações > Desenvolvedor > editar Config`, para encontrar o arquivo**


2. **Adicione o servidor na seção `mcpServers`:**
Configure os caminhos **absolutos** apontando para a pasta onde você clonou o projeto e para o executável Python do seu ambiente virtual.
```json
{
  "mcpServers": {
    "sankhya-mcp": {
      "command": "C:/Caminhos/Para/O/Repositorio/sankhya-mcp/venv/Scripts/python.exe",
      "args": [
        "C:/Caminhos/Para/O/Repositorio/sankhya-mcp/server.py"
      ],
      "env": {
        "SANKHYA_API_URL": "[https://api.sankhya.suaempresa.com.br](https://api.sankhya.suaempresa.com.br)",
        "SANKHYA_USER": "seu_usuario",
        "SANKHYA_PASSWORD": "sua_senha"
      }
    }
  }
}

```


*Dica de TI: Embora você tenha criado o `.env`, preencher o bloco `"env"` diretamente no arquivo `claude_desktop_config.json` é a forma mais garantida de assegurar que o Claude inicie o servidor com as variáveis de ambiente carregadas.*
3. **Reinicie o Claude Desktop.** Se configurado corretamente, o ícone de uma "tomada" aparecerá no Claude informando que as ferramentas (tools) do Sankhya estão ativas.

---

## 🔀 3. Fluxo de Trabalho (Git Flow)

Para mantermos a qualidade do repositório `lucasbCPE/sankhya-mcp` e garantirmos que os arquivos como `baseconhecimento.py` e `server.py`  não sejam sobrepostos, utilizamos uma abordagem de **Git Flow**.

⚠️ CUIDADO: Evite commits diretamente na branch `main`!

Para contribuir, siga estritamente os passos abaixo:

1. **Atualize seu ambiente principal antes de começar:**
```bash
git checkout main
git pull origin main

```


2. **Crie uma nova branch para a sua alteração:**
Utilize prefixos que identifiquem o objetivo (ex: `feature/`, `bugfix/`, `hotfix/`).
```bash
git checkout -b feature/melhoria-metadados-tabela

```


3. **Trabalhe e realize os Commits:**
Faça as alterações necessárias nos arquivos. Ao finalizar:


```bash
git add .
git commit -m "feat: aprimora a exportação de metadados da tabela Sankhya"

```


4. **Suba sua branch para o GitHub:**
```bash
git push origin feature/melhoria-metadados-tabela

```


5. **Abra um Pull Request (PR):**
Acesse o repositório no GitHub (`lucasbCPE/sankhya-mcp` ) e abra um Pull Request apontando sua branch para a `main`.


* Isso nos permite revisar o código em equipe.
* O GitHub detectará conflitos caso você e um colega tenham editado as mesmas linhas do `test.py`, permitindo resolver isso de forma segura antes da integração.




6. **Finalize a tarefa após o Merge:**
Com o PR aprovado e o *Merge* concluído na `main`, atualize sua máquina local:


```bash
git checkout main
git pull origin main
git branch -d feature/melhoria-metadados-tabela # apaga a branch antiga


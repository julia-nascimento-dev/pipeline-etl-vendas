<div align="center">

# Pipeline ETL de Vendas

**Extração, validação e carga de dados comerciais com Python e PostgreSQL.**

<img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white" alt="PostgreSQL" />
<img src="https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white" alt="Pandas" />
<img src="https://img.shields.io/badge/pytest-0A9EDC?style=flat&logo=pytest&logoColor=white" alt="pytest" />

</div>

## Visão geral

Este projeto implementa um pipeline ETL em Python para processar dados de vendas recebidos em arquivos CSV. O fluxo extrai os registros, valida a estrutura e as regras de negócio, separa os dados rejeitados e carrega os registros válidos em um banco PostgreSQL.

O projeto também contempla pontos importantes para a confiabilidade de um processo de integração de dados: logs de execução, controle de credenciais por variáveis de ambiente, carga transacional e comportamento idempotente.

## Arquitetura

```text
Arquivo CSV
    ↓
Extração
    ↓
Validação de estrutura e regras
    ├── Registros inválidos → CSV de rejeitados + motivo
    ↓
Registros válidos
    ↓
Carga transacional (UPSERT)
    ↓
PostgreSQL
```

## Funcionalidades

- leitura de arquivos CSV;
- validação de colunas obrigatórias;
- validação de tipos, campos essenciais e valores positivos;
- separação de registros inválidos com o respectivo motivo da rejeição;
- carga no PostgreSQL com operação UPSERT;
- uso de `order_id` como chave para evitar duplicação em reprocessamentos;
- registro de eventos em console e arquivo de log rotativo;
- testes automatizados para as regras de validação;
- conjunto de dados fictícios para demonstração.

## Tecnologias

| Tecnologia | Utilização |
|---|---|
| Python 3.11+ | Implementação do pipeline |
| Pandas | Leitura e manipulação dos dados |
| PostgreSQL 14+ | Persistência dos registros válidos |
| SQL | Estrutura e operações no banco |
| pytest | Testes automatizados |
| python-dotenv | Leitura de configurações locais, quando definida nas dependências |
| Git e GitHub | Controle de versão |

## Estrutura esperada dos dados

O arquivo de entrada deve conter as seguintes colunas:

| Campo | Descrição / regra |
|---|---|
| `order_id` | Identificador único utilizado na carga |
| `order_date` | Data válida do pedido |
| `customer_id` | Identificador do cliente |
| `product` | Produto relacionado à venda |
| `quantity` | Quantidade maior que zero |
| `unit_price` | Preço unitário maior que zero |
| `region` | Região da venda |

Os campos obrigatórios não podem estar vazios. A chave `order_id` representa a granularidade adotada neste exemplo; em uma fonte real, ela deve ser revisada de acordo com o modelo dos dados recebidos.

## Como executar

### Pré-requisitos

- Python 3.11 ou superior;
- PostgreSQL 14 ou superior.

### 1. Clonar o repositório

```bash
git clone https://github.com/julia-nascimento-dev/pipeline-etl-vendas.git
cd pipeline-etl-vendas
```

### 2. Criar o ambiente virtual

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux ou macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar o banco

Copie o arquivo `.env.example` para `.env` e preencha as variáveis de conexão de acordo com o ambiente PostgreSQL local.

Crie o banco de dados `vendas_etl`. O script é responsável por criar a tabela de destino caso ela ainda não exista.

Não compartilhe o arquivo `.env` nem credenciais reais. O arquivo `.env` deve permanecer fora do controle de versão.

### 5. Executar o pipeline

```bash
python -m src.pipeline --input data/vendas.csv
```

Para processar outro arquivo:

```bash
python -m src.pipeline --input caminho/para/arquivo.csv
```

### 6. Executar os testes

```bash
pytest -q
```

## Validação e tratamento de rejeições

Os registros que não atendem às regras definidas são separados dos registros válidos. O arquivo de rejeitados inclui o motivo pelo qual cada registro não passou pela validação, permitindo investigar problemas na origem sem interromper a análise de todos os demais registros.

A validação contempla, entre outros pontos, presença de campos obrigatórios, integridade dos valores numéricos e validade das datas.

## Carga e idempotência

A carga utiliza uma operação UPSERT baseada em `order_id`. Dessa forma, ao processar novamente um registro com a mesma chave, o pipeline atualiza o registro existente em vez de inserir uma duplicata.

A operação de persistência é transacional, ajudando a manter a consistência dos dados durante a carga.

## Logs e segurança

- eventos de execução são registrados no console e em arquivo rotativo;
- configurações de conexão são fornecidas por variáveis de ambiente;
- dados de demonstração são fictícios;
- credenciais não devem ser inseridas diretamente no código ou publicadas no repositório.

## Limitações conhecidas

O pipeline foi projetado para arquivos CSV de pequeno e médio porte carregados em memória. Para volumes muito grandes, uma evolução possível é implementar processamento em lotes e avaliar mecanismos de carga em massa, como o comando `COPY` do PostgreSQL.

A chave de negócio também deve ser reavaliada quando o pipeline for adaptado a uma fonte real, especialmente se cada pedido puder conter vários itens.

## Competências praticadas

- construção de pipelines ETL;
- validação e qualidade de dados;
- tratamento de registros rejeitados;
- integração Python e PostgreSQL;
- operações SQL e UPSERT;
- idempotência e transações;
- logging;
- testes automatizados;
- configuração segura por variáveis de ambiente.

## Autoria

Desenvolvido por **Julia do Nascimento Pereira**, como projeto de portfólio em Engenharia de Software, com foco em engenharia de dados e automação de processos.

---

<div align="center">
<sub>Projeto de estudo com dados fictícios · 2026</sub>
</div>

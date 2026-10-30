# Pipeline ETL de Vendas

Pipeline de dados em Python para extrair vendas de CSV, validar estrutura e regras de negócio, separar registros rejeitados e carregar os dados válidos no PostgreSQL com segurança para reprocessamento.

## Funcionalidades
- Validação de colunas obrigatórias, tipos, valores positivos e campos essenciais.
- Separação de registros inválidos em CSV com motivo da rejeição.
- Carga transacional no PostgreSQL e chave idempotente (`order_id`): executar o mesmo arquivo novamente atualiza o registro, sem duplicá-lo.
- Logs em console e arquivo rotativo.
- Testes automatizados para regras de validação.
- Dataset fictício para demonstração.

## Arquitetura
`data/vendas.csv` → extração → validação → `data/rejeitados.csv` → carga UPSERT no PostgreSQL.

## Requisitos
Python 3.11+ e PostgreSQL 14+. Crie um ambiente virtual e instale:

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

Copie `.env.example` para `.env`, ajuste a conexão e crie o banco `vendas_etl`. O script cria a tabela se ela não existir.

```bash
python -m src.pipeline --input data/vendas.csv
pytest -q
```

Para apontar outro arquivo: `python -m src.pipeline --input caminho/arquivo.csv`.

## Esquema esperado
`order_id`, `order_date`, `customer_id`, `product`, `quantity`, `unit_price`, `region`. `order_id` identifica unicamente um pedido/linha de venda. Quantidade e preço devem ser positivos; data precisa ser válida; campos obrigatórios não podem ficar vazios.

## Segurança e decisões
Credenciais ficam em variáveis de ambiente, nunca no código. O CSV de exemplo contém somente dados fictícios. Em um cenário real, ajuste a chave de negócio conforme a granularidade da origem (pedido ou item do pedido).

## Estrutura
```text
src/       pipeline e validação
sql/       DDL do banco
data/     CSV fictício e rejeitados gerados
logs/      logs de execução
 tests/    testes automatizados
```

## Limitações conhecidas
O pipeline foi pensado para CSVs de porte pequeno/médio carregados em memória. Para milhões de linhas, considere processamento em lotes e COPY do PostgreSQL. Execute `pytest` no ambiente configurado antes de publicar resultados de execução.

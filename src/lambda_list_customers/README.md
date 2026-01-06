# Lambda List Customers

Lambda responsável por listar clientes do tipo CUSTOMER a partir do RDS.

## Funcionalidades

- ✅ Listar clientes com paginação
- ✅ Filtrar por status (exato)
- ✅ Filtrar por email (parcial, case-insensitive)
- ✅ Ordenar por data de criação (desc)
- ✅ Retornar metadados de paginação
- ✅ Retornar apenas campos necessários

## Estrutura de Pastas

```
lambda_list_customers/
├── handler.py                          # Handler principal
├── strategies/
│   ├── base.py                         # Classe base abstrata
│   └── list_customers_strategy.py      # Lógica de listagem
├── utils/
│   ├── db_client.py                    # Cliente PostgreSQL
│   └── responses.py                    # Helper de respostas HTTP
├── Dockerfile
├── requirements.txt
└── test_local.py                       # Script para testes locais
```

## Variáveis de Ambiente

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `DB_HOST` | Host e porta do PostgreSQL | `localhost:5432` |
| `DB_USER` | Usuário do banco de dados | `postgres` |
| `DB_PASSWORD` | Senha do banco de dados | `senha123` |
| `DB_NAME` | Nome do banco de dados | `pos_db` |
| `CUSTOMER_TABLE` | Nome da tabela de clientes | `customers` (padrão) |

## Parâmetros de Request

### Paginação
- **`page`** (opcional): Número da página (default: 1, mínimo: 1)
- **`per_page`** (opcional): Registros por página (default: 20, mínimo: 1, máximo: 100)

### Filtros
- **`status`** (opcional): Filtrar por status exato (ex: "active", "inactive")
- **`email`** (opcional): Filtrar por email (busca parcial, case-insensitive)

## Request/Response

### Request - Listagem Simples
```
GET /customers?page=1&per_page=10
```

### Request - Com Filtros
```
GET /customers?page=1&per_page=20&status=active&email=john
```

### Response - Sucesso (200)
```json
{
  "message": "Clientes listados com sucesso",
  "customers": [
    {
      "id": "123",
      "cognito_user_id": "cognito-123",
      "cpf": "12345678900",
      "email": "customer@example.com",
      "name": "John Doe",
      "status": "active",
      "created_at": "2026-01-06T10:00:00",
      "updated_at": "2026-01-06T10:00:00"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total_records": 45,
    "total_pages": 5,
    "has_next": true,
    "has_previous": false
  }
}
```

### Response - Lista Vazia (200)
```json
{
  "message": "Clientes listados com sucesso",
  "customers": [],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total_records": 0,
    "total_pages": 0,
    "has_next": false,
    "has_previous": false
  }
}
```

### Response - Parâmetros Inválidos (400)
```json
{
  "message": "Parâmetros de paginação inválidos. 'page' e 'per_page' devem ser números inteiros"
}
```

### Response - Erro Interno (500)
```json
{
  "message": "Erro interno ao listar clientes: <detalhes do erro>"
}
```

## Metadados de Paginação

O response sempre inclui um objeto `pagination` com:

- **`page`**: Página atual
- **`per_page`**: Registros por página
- **`total_records`**: Total de registros encontrados (considerando filtros)
- **`total_pages`**: Total de páginas disponíveis
- **`has_next`**: Boolean indicando se existe próxima página
- **`has_previous`**: Boolean indicando se existe página anterior

## Campos Retornados

Para otimizar a performance, apenas os seguintes campos são retornados:

- `id`: Identificador único do cliente
- `cognito_user_id`: ID do usuário no Cognito
- `cpf`: CPF do cliente
- `email`: Email do cliente
- `name`: Nome completo do cliente
- `status`: Status do cliente (active, inactive, etc)
- `created_at`: Data de criação do registro
- `updated_at`: Data da última atualização

## Ordenação

Os resultados são sempre ordenados por `created_at DESC` (mais recentes primeiro).

## Teste Local

```bash
python test_local.py
```

## Build Docker

```bash
docker build -t lambda-list-customers .
```

## Logging

O Lambda utiliza logging estruturado em todos os níveis:

- Evento recebido do API Gateway
- Parâmetros extraídos (query params ou body)
- Queries SQL executadas
- Total de registros encontrados
- Erros e exceções detalhadas

## Boas Práticas Implementadas

✅ Separação de responsabilidades (handler / strategy / utils)  
✅ Validação de parâmetros de paginação  
✅ Limites de paginação (máximo 100 registros por página)  
✅ Queries otimizadas (SELECT apenas campos necessários)  
✅ Contagem total separada para metadados  
✅ Remoção de dados sensíveis  
✅ Logging estruturado  
✅ Tratamento de erros com códigos HTTP apropriados  
✅ Suporte para filtros opcionais  
✅ Busca case-insensitive para email  
✅ Default values para parâmetros opcionais  

## Performance

- **Query de contagem**: Executa `COUNT(*)` com os mesmos filtros para obter total de registros
- **Query de dados**: Usa `LIMIT` e `OFFSET` para paginação eficiente
- **Índices recomendados**: 
  - `created_at` (para ordenação)
  - `status` (para filtros)
  - `email` (para filtros e buscas)

## Segurança

- Queries parametrizadas para prevenir SQL injection
- Dados sensíveis (passwords) removidos da resposta
- Validação de tipos de dados nos parâmetros
- Limites de paginação para prevenir sobrecarga

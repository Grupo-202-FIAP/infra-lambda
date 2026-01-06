# Lambda Get Customer

Lambda responsável por buscar um cliente no RDS.

## Funcionalidades
- Buscar cliente por customer_id, email ou cpf
- Validar que o usuário é do tipo CUSTOMER
- Retornar 404 quando não encontrar
- Retornar 400 para parâmetros inválidos

## Arquitetura

Este Lambda segue o padrão arquitetural do projeto:
- **Handler**: Ponto de entrada que processa o evento do API Gateway
- **Strategy**: Implementa a lógica de negócio de busca no RDS
- **Utils**: Componentes reutilizáveis (db_client, responses)
- **Tests**: Testes unitários completos com mocks

## Estrutura de Pastas

```
lambda_get_customer/
├── handler.py                              # Handler principal
├── strategies/
│   ├── __init__.py
│   ├── base.py                             # Classe base abstrata
│   └── get_customer_strategy.py            # Lógica de busca
├── utils/
│   ├── __init__.py
│   ├── db_client.py                        # Cliente PostgreSQL
│   └── responses.py                        # Helper de respostas HTTP
├── tests/
│   ├── __init__.py
│   ├── conftest.py                         # Fixtures do pytest
│   ├── test_handler.py                     # Testes do handler
│   └── test_get_customer_strategy.py       # Testes da strategy
├── Dockerfile
├── requirements.txt
└── test_local.py                           # Script para testes locais
```

## Variáveis de Ambiente

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `DB_HOST` | Host e porta do PostgreSQL | `localhost:5432` |
| `DB_USER` | Usuário do banco de dados | `postgres` |
| `DB_PASSWORD` | Senha do banco de dados | `senha123` |
| `DB_NAME` | Nome do banco de dados | `pos_db` |
| `CUSTOMER_TABLE` | Nome da tabela de clientes | `customers` (padrão) |

## Request/Response

### Request (via Query Parameters)
```json
GET /customers?customer_id=123
GET /customers?email=test@example.com
GET /customers?cpf=12345678900
```

### Request (via Body)
```json
POST /customers
{
  "customer_id": "123"
}
```

### Response - Sucesso (200)
```json
{
  "message": "Cliente encontrado com sucesso",
  "customer": {
    "id": "123",
    "cognito_user_id": "cognito-123",
    "cpf": "12345678900",
    "email": "test@example.com",
    "name": "John Doe"
  }
}
```

### Response - Cliente Não Encontrado (404)
```json
{
  "message": "Cliente não encontrado"
}
```

### Response - Parâmetros Inválidos (400)
```json
{
  "message": "É necessário fornecer pelo menos um parâmetro de busca: customer_id, email ou cpf"
}
```

### Response - Erro Interno (500)
```json
{
  "message": "Erro interno ao buscar cliente: <detalhes do erro>"
}
```

## Instalação

```bash
pip install -r requirements.txt
```

## Testes

### Executar testes unitários
```bash
pytest tests/ -v
```

### Executar testes com coverage
```bash
pytest tests/ --cov=. --cov-report=html
```

### Teste local
```bash
python test_local.py
```

## Build Docker

```bash
docker build -t lambda-get-customer .
```

## Deploy

O Lambda pode ser deployado usando Terraform, AWS SAM, ou AWS CLI.

Exemplo com AWS CLI:
```bash
aws lambda update-function-code \
  --function-name lambda-get-customer \
  --image-uri <ECR_URI>:latest
```

## Logging

O Lambda utiliza o módulo `logging` do Python com nível INFO. Logs incluem:
- Evento recebido
- Parâmetros extraídos
- Query executada
- Resultado da busca
- Erros e exceções

## Integração com RDS

O Lambda conecta-se diretamente ao PostgreSQL RDS usando `psycopg2`. A classe `DBClient` gerencia:
- Conexão com o banco
- Validação de variáveis de ambiente
- Execução de queries (write e read)
- Logging de operações

## Boas Práticas Implementadas

✅ Separação de responsabilidades (handler / strategy / utils)  
✅ Logging estruturado em todos os níveis  
✅ Tratamento de erros com códigos HTTP apropriados  
✅ Validação de parâmetros de entrada  
✅ Remoção de dados sensíveis da resposta  
✅ Testes unitários com mocks  
✅ Suporte para múltiplos métodos de busca  
✅ Configuração via variáveis de ambiente  
✅ Compatível com API Gateway  

## Segurança

- Dados sensíveis (como passwords) são removidos da resposta
- Conexões com RDS devem usar SSL em produção
- Credenciais do banco devem ser gerenciadas via AWS Secrets Manager ou SSM Parameter Store
- Lambda deve ter role IAM com permissões mínimas necessárias

## Próximos Passos

- Implementar paginação para buscas que retornam múltiplos resultados
- Adicionar filtros adicionais (status, data de criação, etc)
- Implementar cache com ElastiCache/Redis para melhorar performance
- Adicionar métricas customizadas no CloudWatch

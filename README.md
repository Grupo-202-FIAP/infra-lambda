# Infra Lambda - Sistema de Autenticação e Gerenciamento de Usuários

Repositório contendo a infraestrutura e código-fonte das AWS Lambdas para autenticação e gerenciamento de usuários, utilizando Terraform e AWS Cognito.

---
youtyoutube youtube sd
## 📁 Estrutura do Projeto

```
infra-lambda/
├── infra/                          # Infraestrutura Terraform
│   ├── main.tf                     # Configuração principal
│   ├── variables.tf                # Variáveis do projeto
│   ├── outputs.tf                  # Outputs do Terraform
│   ├── provider.tf                 # Configuração do provider AWS
│   ├── terraform.tfvars            # Valores das variáveis
│   └── modules/                    # Módulos Terraform
│       ├── cognito_user_pool_customer/   # User Pool de clientes
│       ├── cognito_user_pool_internal/   # User Pool de usuários internos
│       ├── iam/                          # Roles e Policies
│       ├── lambda_auth/                  # Lambda de autenticação
│       ├── lambda_get_user/              # Lambda de busca de usuário
│       ├── lambda_list_users/            # Lambda de listagem de usuários
│       └── lambda_registration/          # Lambda de registro
│
└── src/                            # Código-fonte das Lambdas
    ├── lambda_auth/                # Autenticação de usuários
    ├── lambda_get_user/            # Busca de usuário por ID/email/CPF
    ├── lambda_list_users/          # Listagem paginada de usuários
    └── lambda_registration/        # Registro de novos usuários
```

---

## 🚀 Lambdas Disponíveis

### 1. Lambda Auth (`lambda_auth`)
Responsável pela autenticação de usuários (customers e internal).

### 2. Lambda Registration (`lambda_registration`)
Responsável pelo registro de novos usuários no sistema.

### 3. Lambda Get User (`lambda_get_user`)
Busca um usuário específico por ID, email ou CPF.

### 4. Lambda List Users (`lambda_list_users`)
Lista todos os usuários com suporte a paginação e filtros.

---

## 📋 Pré-requisitos

- **AWS CLI** configurado
- **Terraform** >= 1.0
- **Docker** (para build das imagens Lambda)
- **Python** 3.9+

---

## ⚙️ Variáveis de Ambiente

| Variável | Descrição |
|----------|-----------|
| `REGION` | Região AWS (default: `us-east-1`) |
| `CUSTOMER_USER_POOL` | ID do User Pool de clientes |
| `INTERNAL_USER_POOL_ID` | ID do User Pool interno |
| `INTERNAL_APP_CLIENT_ID` | Client ID do App interno |
| `JWT_SECRET` | Secret para geração de tokens JWT |
| `CUSTOMER_TABLE` | Nome da tabela de customers no banco |
| `INTERNAL_TABLE` | Nome da tabela de usuários internos |

---

## 📡 Exemplos de Requisições das Lambdas

### 1. Lambda Auth - Autenticação

#### 1.1 Autenticação de Customer (por CPF)

**Request:**
```bash
curl -X POST https://<API_GATEWAY_URL>/auth \
  -H "Content-Type: application/json" \
  -H "x-correlation-id: 123e4567-e89b-12d3-a456-426614174000" \
  -d '{
    "type": "customer",
    "cpf": "12345678901"
  }'
```

**Response (200 - Sucesso):**
```json
{
  "message": "Autenticação por CPF bem-sucedida",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "role": "ROLE_CUSTOMER",
  "userId": "12345678901"
}
```

**Response (404 - Cliente não encontrado):**
```json
{
  "message": "Cliente não encontrado"
}
```

---

#### 1.2 Autenticação Interna (por Email/Senha)

**Request:**
```bash
curl -X POST https://<API_GATEWAY_URL>/auth \
  -H "Content-Type: application/json" \
  -H "x-correlation-id: 123e4567-e89b-12d3-a456-426614174000" \
  -d '{
    "type": "internal",
    "email": "admin@empresa.com",
    "password": "SenhaSegura123!"
  }'
```

**Response (200 - Sucesso):**
```json
{
  "message": "Login interno bem-sucedido",
  "idToken": "eyJraWQiOiI...",
  "accessToken": "eyJraWQiOiI...",
  "refreshToken": "eyJjdHkiOiI...",
  "role": "ROLE_EMPLOYEE"
}
```

**Response (403 - Troca de senha necessária):**
```json
{
  "message": "Usuário precisa trocar a senha",
  "challenge": "NEW_PASSWORD_REQUIRED",
  "session": "AYABeC..."
}
```

#### 1.3 Autenticação Interna com Troca de Senha

**Request:**
```bash
curl -X POST https://<API_GATEWAY_URL>/auth \
  -H "Content-Type: application/json" \
  -d '{
    "type": "internal",
    "email": "admin@empresa.com",
    "password": "SenhaTemporaria123!",
    "new_password": "NovaSenhaSegura456!"
  }'
```

---

### 2. Lambda Registration - Registro de Usuários

#### 2.1 Registro de Customer

**Request:**
```bash
curl -X POST https://<API_GATEWAY_URL>/register \
  -H "Content-Type: application/json" \
  -H "x-correlation-id: 123e4567-e89b-12d3-a456-426614174000" \
  -d '{
    "type": "customer",
    "cpf": "12345678901",
    "email": "cliente@email.com",
    "name": "João Silva"
  }'
```

**Response (201 - Sucesso):**
```json
{
  "message": "Customer cadastrado e sincronizado com sucesso",
  "registration": {
    "message": "Cliente cadastrado com sucesso",
    "userId": "12345678901"
  },
  "sync": {
    "message": "Dados sincronizados com sucesso"
  }
}
```

**Response (409 - Cliente já cadastrado):**
```json
{
  "message": "Cliente já cadastrado"
}
```

---

#### 2.2 Registro de Usuário Interno

**Request:**
```bash
curl -X POST https://<API_GATEWAY_URL>/register \
  -H "Content-Type: application/json" \
  -H "x-correlation-id: 123e4567-e89b-12d3-a456-426614174000" \
  -d '{
    "type": "internal",
    "email": "funcionario@empresa.com",
    "password": "SenhaSegura123!",
    "name": "Maria Santos"
  }'
```

**Response (201 - Sucesso):**
```json
{
  "message": "Internal cadastrado e sincronizado com sucesso",
  "registration": {
    "message": "Usuário interno cadastrado com sucesso",
    "userId": "funcionario@empresa.com"
  },
  "sync": {
    "message": "Dados sincronizados com sucesso"
  }
}
```

**Response (409 - Usuário já cadastrado):**
```json
{
  "message": "Usuário interno já cadastrado"
}
```

---

### 3. Lambda Get User - Busca de Usuário

#### 3.1 Busca por ID

**Request:**
```bash
curl -X GET "https://<API_GATEWAY_URL>/users?user_id=550e8400-e29b-41d4-a716-446655440000" \
  -H "x-correlation-id: 123e4567-e89b-12d3-a456-426614174000"
```

**Response (200 - Sucesso):**
```json
{
  "message": "Usuário encontrado com sucesso",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "cognito_user_id": "12345678901",
    "email": "cliente@email.com",
    "name": "João Silva",
    "cpf": "12345678901",
    "status": "ACTIVE",
    "type": "customer",
    "created_at": "2025-01-10T10:00:00Z",
    "updated_at": "2025-01-10T10:00:00Z"
  }
}
```

---

#### 3.2 Busca por Email

**Request:**
```bash
curl -X GET "https://<API_GATEWAY_URL>/users?email=cliente@email.com" \
  -H "x-correlation-id: 123e4567-e89b-12d3-a456-426614174000"
```

---

#### 3.3 Busca por CPF

**Request:**
```bash
curl -X GET "https://<API_GATEWAY_URL>/users?cpf=12345678901" \
  -H "x-correlation-id: 123e4567-e89b-12d3-a456-426614174000"
```

---

#### 3.4 Busca via Body (POST)

**Request:**
```bash
curl -X POST https://<API_GATEWAY_URL>/users \
  -H "Content-Type: application/json" \
  -H "x-correlation-id: 123e4567-e89b-12d3-a456-426614174000" \
  -d '{
    "email": "cliente@email.com"
  }'
```

**Response (404 - Não encontrado):**
```json
{
  "message": "Usuário não encontrado"
}
```

---

### 4. Lambda List Users - Listagem de Usuários

#### 4.1 Listagem Simples (com paginação padrão)

**Request:**
```bash
curl -X GET "https://<API_GATEWAY_URL>/users/list" \
  -H "x-correlation-id: 123e4567-e89b-12d3-a456-426614174000"
```

**Response (200 - Sucesso):**
```json
{
  "message": "Usuários listados com sucesso",
  "users": [
    {
      "type": "customer",
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "cognito_user_id": "12345678901",
      "cpf": "12345678901",
      "email": "cliente@email.com",
      "name": "João Silva",
      "status": "ACTIVE",
      "created_at": "2025-01-10T10:00:00Z",
      "updated_at": "2025-01-10T10:00:00Z"
    },
    {
      "type": "internal",
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "cognito_user_id": "admin@empresa.com",
      "cpf": null,
      "email": "admin@empresa.com",
      "name": "Admin User",
      "status": null,
      "created_at": "2025-01-09T08:00:00Z",
      "updated_at": "2025-01-09T08:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total_records": 2,
    "total_pages": 1,
    "has_next": false,
    "has_previous": false
  }
}
```

---

#### 4.2 Listagem com Paginação

**Request:**
```bash
curl -X GET "https://<API_GATEWAY_URL>/users/list?page=2&per_page=10" \
  -H "x-correlation-id: 123e4567-e89b-12d3-a456-426614174000"
```

---

#### 4.3 Listagem com Filtro por Status

**Request:**
```bash
curl -X GET "https://<API_GATEWAY_URL>/users/list?status=ACTIVE" \
  -H "x-correlation-id: 123e4567-e89b-12d3-a456-426614174000"
```

---

#### 4.4 Listagem com Filtro por Email

**Request:**
```bash
curl -X GET "https://<API_GATEWAY_URL>/users/list?email=empresa.com" \
  -H "x-correlation-id: 123e4567-e89b-12d3-a456-426614174000"
```

---

#### 4.5 Listagem via Body (POST)

**Request:**
```bash
curl -X POST https://<API_GATEWAY_URL>/users/list \
  -H "Content-Type: application/json" \
  -H "x-correlation-id: 123e4567-e89b-12d3-a456-426614174000" \
  -d '{
    "page": 1,
    "per_page": 50,
    "status": "ACTIVE",
    "email": "empresa.com"
  }'
```

---

## 🛠️ Deploy

### 1. Build das Imagens Docker

```bash
# Lambda Auth
cd src/lambda_auth
docker build -t lambda-auth:latest .

# Lambda Registration
cd src/lambda_registration
docker build -t lambda-registration:latest .

# Lambda Get User
cd src/lambda_get_user
docker build -t lambda-get-user:latest .

# Lambda List Users
cd src/lambda_list_users
docker build -t lambda-list-users:latest .
```

### 2. Push para ECR

```bash
# Login no ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

# Tag e push
docker tag lambda-auth:latest <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/lambda-auth:latest
docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/lambda-auth:latest
```

### 3. Deploy com Terraform

```bash
cd infra

# Inicializar Terraform
terraform init

# Verificar plano de execução
terraform plan

# Aplicar infraestrutura
terraform apply
```

---

## 🧪 Testes

```bash
# Instalar dependências de teste
pip install -r requirements.txt
pip install pytest pytest-cov

# Executar testes
cd src/lambda_auth
pytest tests/ -v

cd src/lambda_registration
pytest tests/ -v

cd src/lambda_get_user
pytest tests/ -v

cd src/lambda_list_users
pytest tests/ -v
```

---

## 📊 Códigos de Resposta HTTP

| Código | Descrição |
|--------|-----------|
| `200` | Sucesso |
| `201` | Criado com sucesso |
| `400` | Requisição inválida (campos obrigatórios ausentes) |
| `401` | Não autorizado |
| `403` | Proibido (ex: troca de senha necessária) |
| `404` | Recurso não encontrado |
| `409` | Conflito (ex: usuário já existe) |
| `500` | Erro interno do servidor |

---

## 🔒 Tipos de Usuário

| Tipo | Descrição | Autenticação |
|------|-----------|--------------|
| `customer` | Cliente externo | CPF |
| `internal` | Funcionário interno | Email + Senha |

---

## 📝 Headers Suportados

| Header | Descrição | Obrigatório |
|--------|-----------|-------------|
| `Content-Type` | `application/json` | Sim (POST) |
| `x-correlation-id` | ID de correlação para rastreamento | Não |

---

## 📄 Licença

Este projeto é proprietário e de uso interno.

# ==========================
# Configuração geral
# ==========================
variable "project_name" {
  description = "Nome do projeto ou aplicação principal (usado para prefixar recursos)."
  type        = string
}

variable "aws_region" {
  description = "Região da AWS onde os recursos serão criados."
  type        = string
  default     = "us-east-1"
}

variable "account_id" {
  description = "ID da conta AWS utilizada para o deploy dos recursos."
  type        = string
}


# ==========================
# Lambda Authorizers
# ==========================
variable "authorizer_name" {
  description = "Nome da função Lambda Authorizer."
  type        = string
}

variable "lambda_image_tag" {
  description = "A tag da imagem Docker enviada para o ECR (ex: latest, v1.0.0) que as Lambdas devem usar."
  type        = string
  default     = "latest"
}

variable "package_type" {
  description = "Tipo de pacote da Lambda (ex: 'Zip' ou 'Image')."
  type        = string
}

variable "memory_size" {
  description = "Quantidade de memória alocada (em MB) para a função Lambda."
  type        = number
}

variable "timeout" {
  description = "Tempo máximo de execução da função Lambda, em segundos."
  type        = number
}


# ==========================
# Lambda Registration/Sync
# ==========================
variable "lambda_registration_name" {
  description = "Nome da função Lambda unificada responsável pelo registro e sincronização (Customer e Internal)."
  type        = string
}

# ==========================
# Lambda Get/List Users
# ==========================
variable "lambda_get_user_name" {
  description = "Nome da função Lambda responsável por buscar usuários (customer/internal)."
  type        = string
}

variable "lambda_list_users_name" {
  description = "Nome da função Lambda responsável por listar usuários (customer/internal)."
  type        = string
}

variable "db_host" {
  description = "Host e porta do banco (ex: host:5432)."
  type        = string
}

variable "db_user" {
  description = "Usuário do banco de dados."
  type        = string
}

variable "db_password" {
  description = "Senha do banco de dados."
  type        = string
}

variable "db_name" {
  description = "Nome do banco de dados."
  type        = string
}

variable "customer_table" {
  description = "Nome da tabela de customers."
  type        = string
  default     = "customers"
}

variable "internal_table" {
  description = "Nome da tabela de usuários internos."
  type        = string
  default     = "internal_users"
}

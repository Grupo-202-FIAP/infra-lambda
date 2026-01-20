variable "user_pools" {
  type = map(string)
}

variable "account_id" {
  description = "ID da conta AWS onde os recursos serão criados."
  type        = string
}

variable "lambda_runtime" {
  description = "Runtime da Lambda"
  type        = string
}

variable "region" {
  description = "Região AWS"
  type        = string
}

variable "authorizer_customer_name" {
  description = "Nome da função Lambda Authorizer para clientes externos."
  type        = string
}

variable "authorizer_customer_output_path" {
  description = "Caminho local para o arquivo .zip de deploy do Authorizer Customer."
  type        = string
}

variable "authorizer_customer_handler" {
  description = "Nome do handler da função Authorizer Customer (ex: arquivo.funcao)."
  type        = string
}

variable "lambda_archive_type" {
  description = "Tipo de arquivo do pacote de código Lambda (ex: zip, Image)."
  type        = string
}
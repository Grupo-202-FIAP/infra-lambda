variable "user_pools" {
  description = "Mapa com os IDs dos user pools."
  type        = map(string)
}

variable "internal_app_client_id" {
  description = "App Client ID do pool internal."
  type        = string
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
variable "authorizer_internal_name" {
  description = "Nome da função Lambda Authorizer para usuários internos/admin."
  type        = string
}

variable "authorizer_internal_output_path" {
  description = "Caminho local para o arquivo .zip de deploy do Authorizer Internal."
  type        = string
}

variable "authorizer_internal_handler" {
  description = "Nome do handler da função Authorizer Internal."
  type        = string
}

variable "lambda_archive_type" {
  description = "Tipo de arquivo do pacote de código Lambda (ex: zip, Image)."
  type        = string
}

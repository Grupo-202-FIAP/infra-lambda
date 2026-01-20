variable "lambda_source_dir" {
  description = "Diretório do código da Lambda"
  type        = string
}

variable "lambda_runtime" {
  description = "Runtime da Lambda"
  type        = string
}

variable "lambda_memory_size" {
  description = "Memória da Lambda"
  type        = number
  default     = 128
}

variable "lambda_timeout" {
  description = "Timeout da Lambda"
  type        = number
  default     = 10
}

variable "region" {
  description = "Região AWS"
  type        = string
}

variable "user_pools" {
  description = "Mapeamento dos user pools"
  type        = map(string)
}

variable "account_id" {
  description = "ID da conta AWS onde os recursos serão criados."
  type        = string
}

variable "registration_customer_name" {
  description = "Nome da função Lambda para o registro de clientes externos."
  type        = string
}

variable "registration_customer_output_path" {
  description = "Caminho local para o arquivo .zip de deploy do Registration Customer."
  type        = string
}

variable "registration_customer_handler" {
  description = "Nome do handler da função Registration Customer."
  type        = string
}

variable "lambda_archive_type" {
  description = "Tipo de arquivo do pacote de código Lambda (ex: zip, Image)."
  type        = string
}

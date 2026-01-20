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

variable "account_id" {
  description = "ID da conta AWS onde os recursos serão criados."
  type        = string
}

variable "sync_internal_name" {
  description = "Nome da função Lambda para o registro de usuários internos/admin."
  type        = string
}

variable "sync_internal_output_path" {
  description = "Caminho local para o arquivo .zip de deploy do Registration Internal."
  type        = string
}

variable "sync_internal_handler" {
  description = "Nome do handler da função Registration Internal."
  type        = string
}

variable "lambda_archive_type" {
  description = "Tipo de arquivo do pacote de código Lambda (ex: zip, Image)."
  type        = string
}

variable "subnet_ids" {
  description = "Lista de subnets privadas para rodar a Lambda dentro da VPC"
  type        = list(string)
}

variable "security_group_ids" {
  description = "Lista de Security Groups que a Lambda deve usar"
  type        = list(string)
}


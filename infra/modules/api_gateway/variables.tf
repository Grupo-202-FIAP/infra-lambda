variable "name" {
  description = "API Gateway Tech challenge"
  type        = string
  default = "crud-api"
}

variable "description" {
  description = "Descrição do API Gateway"
  type        = string
  default     = "API Gateway gerenciado pelo Terraform"
}

variable "root_path" {
  description = "Path raiz do recurso do API Gateway"
  type        = string
  default     = "items"
}

variable "stage_name" {
  description = "Nome do stage para o deployment"
  type        = string
  default     = "dev"
}

variable "lambda_authorizer_invoke_arn" {
  description = "ARN de invocação da função Lambda Authorizer"
  type        = string
}

variable "lambda_registration_invoke_arn" {
  description = "ARN de invocação da função Lambda Registration"
  type        = string
}

variable "lambda_authorizer_name" {
  description = "Nome da função Lambda Authorizer"
  type        = string
}

variable "lambda_registration_name" {
  description = "Nome da função Lambda Registration"
  type        = string
}

variable "lambda_auth_internal_invoke_arn" {
  description = "ARN de invocação da função Lambda Auth Internal"
  type        = string
}

variable "lambda_register_internal_invoke_arn" {
  description = "ARN de invocação da função Lambda Register Internal"
  type        = string
}

variable "lambda_auth_internal_name" {
  description = "Nome da função Lambda Auth Internal"
  type        = string
}

variable "lambda_register_internal_name" {
  description = "Nome da função Lambda Register Internal"
  type        = string
}

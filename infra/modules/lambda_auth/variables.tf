variable "function_name" {
  type        = string
  description = "Nome da função Lambda"
}

variable "account_id" {
  type        = string
  description = "ID da conta AWS onde a Lambda será criada"
}

variable "environment_variables" {
  type        = map(string)
  description = "Mapa de variáveis de ambiente da Lambda"
}

variable "role_arn" {
  type        = string
  description = "ARN da IAM Role que a Lambda vai assumir"
}

variable "lambda_auth_image_tag" {
  description = "A tag da imagem Docker enviada para o ECR (ex: latest, v1.0.0)"
  type        = string
  default     = "latest" 
}

variable "package_type" {
  description = "Tipo de pacote de deployment da função Lambda (Zip ou Image)."
  type        = string
}

variable "memory_size" {
  description = "Quantidade de memória em MB para a função Lambda."
  type        = number
}

variable "timeout" {
  description = "Tempo máximo de execução da função Lambda em segundos."
  type        = number
}

variable "image_uri" {
  description = "URI da imagem Docker no ECR."
  type        = string
}

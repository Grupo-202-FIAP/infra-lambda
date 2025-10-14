variable "aws_region" {
  description = "Região da AWS"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Nome do projeto ou aplicação principal (usado para prefixar recursos)."
  type        = string
}


variable "account_id" {
  type        = string
  description = "ID da conta AWS onde a Lambda será criada"
}

variable "authorizer_customer_name" {
  description = "Nome da função Lambda Authorizer para clientes externos."
  type        = string
}

variable "authorizer_internal_name" {
  description = "Nome da função Lambda Authorizer para usuários internos/admin."
  type        = string
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

variable "lambda_auth_image_tag" {
  description = "A tag da imagem Docker enviada para o ECR (ex: latest, v1.0.0) que as Lambdas Authorizer devem usar."
  type        = string
  default     = "latest" 
} 


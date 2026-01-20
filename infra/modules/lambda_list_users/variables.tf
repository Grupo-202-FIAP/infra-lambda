variable "function_name" {
  description = "Nome da função Lambda a ser criada."
  type        = string
}

variable "role_arn" {
  description = "ARN da role IAM que a Lambda irá assumir."
  type        = string
}

variable "role_name" {
  description = "Nome da role IAM usada para anexar a política básica da Lambda."
  type        = string
}

variable "package_type" {
  description = "Tipo de pacote da Lambda (Zip ou Image)."
  type        = string
}

variable "image_uri" {
  description = "URI da imagem Docker para a Lambda (usado quando package_type = 'Image')."
  type        = string
}

variable "memory_size" {
  description = "Quantidade de memória (em MB) alocada para a Lambda."
  type        = number
}

variable "timeout" {
  description = "Tempo máximo de execução da Lambda, em segundos."
  type        = number
}

variable "subnet_ids" {
  description = "Lista de subnets privadas onde a Lambda será implantada (VPC)."
  type        = list(string)
}

variable "security_group_ids" {
  description = "Lista de Security Groups que serão associados à Lambda."
  type        = list(string)
}

variable "environment_variables" {
  description = "Mapa de variáveis de ambiente que serão definidas na Lambda."
  type        = map(string)
}

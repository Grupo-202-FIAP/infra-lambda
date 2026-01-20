variable "project_name" {
  description = "Nome do projeto para prefixar recursos"
  type        = string
}

variable "internal_app_client_name" {
  description = "Nome do App Client para usuários internos (Internal/Admin)"
  type        = string
  default     = "internal-client"
}
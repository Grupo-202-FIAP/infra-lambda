variable "project_name" {
  description = "Nome do projeto para prefixar recursos"
  type        = string
}

variable "internal_app_client_name" {
  description = "Nome do App Client para usuários internos (Employee/Admin)"
  type        = string
  default     = "internal-client"
}
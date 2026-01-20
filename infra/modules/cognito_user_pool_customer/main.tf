resource "aws_cognito_user_pool" "customer" {
  name = "${var.project_name}-customer-pool"

  # Login por CPF (custom auth)
  username_attributes      = [] #
  auto_verified_attributes = []

  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_uppercase = true
    require_numbers   = true
    require_symbols   = true
  }

  schema {
    name                     = "cpf"
    attribute_data_type      = "String"
    developer_only_attribute = false
    mutable                  = false
    required                 = false
    string_attribute_constraints {
      min_length = 11
      max_length = 14
    }
  }
}

# App Client para Customer
resource "aws_cognito_user_pool_client" "customer" {
  name         = var.customer_app_client_name
  user_pool_id = aws_cognito_user_pool.customer.id

  # Habilita custom auth (para autenticação via CPF)
  explicit_auth_flows = ["ALLOW_CUSTOM_AUTH", "ALLOW_REFRESH_TOKEN_AUTH"]

  generate_secret = false
}

# Grupo para Customer
resource "aws_cognito_user_group" "customer" {
  name         = "ROLE_CUSTOMER"
  user_pool_id = aws_cognito_user_pool.customer.id
}

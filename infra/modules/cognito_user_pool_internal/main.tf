resource "aws_cognito_user_pool" "internal" {
  name = "${var.project_name}-internal-pool"

  # Login via email
  username_attributes = ["email"]

  auto_verified_attributes = ["email"]

  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_uppercase = true
    require_numbers   = true
    require_symbols   = true
  }

  schema {
    name                = "email"
    attribute_data_type = "String"
    mutable             = true
    required            = true
  }

}

# App Client para Employee/Admin
resource "aws_cognito_user_pool_client" "internal" {
  name         = var.internal_app_client_name
  user_pool_id = aws_cognito_user_pool.internal.id

  explicit_auth_flows = ["ALLOW_USER_PASSWORD_AUTH", "ALLOW_REFRESH_TOKEN_AUTH", "ALLOW_ADMIN_USER_PASSWORD_AUTH"]

  generate_secret = false

  access_token_validity  = 60 # minutos (5–60)
  id_token_validity      = 60 # minutos (5–60)
  refresh_token_validity = 30 # dias (1–3650)
  token_validity_units {
    access_token  = "minutes"
    id_token      = "minutes"
    refresh_token = "days"
  }
}

# Grupos para Internal
resource "aws_cognito_user_group" "employee" {
  name         = "ROLE_EMPLOYEE"
  user_pool_id = aws_cognito_user_pool.internal.id
}

resource "aws_cognito_user_group" "admin" {
  name         = "ROLE_ADMIN"
  user_pool_id = aws_cognito_user_pool.internal.id
}

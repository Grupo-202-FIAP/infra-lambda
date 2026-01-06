project_name     = "nextime-app"
aws_region       = "us-east-1"
account_id       = "056075870573"
package_type     = "Image"
memory_size      = "512"
timeout          = "30"
lambda_image_tag = "latest"


authorizer_name          = "lambda_authorizer"
lambda_registration_name = "lambda_registration"

# New Lambdas (users)
lambda_get_user_name     = "lambda_get_user"
lambda_list_users_name   = "lambda_list_users"

# Database configuration for user lambdas
db_host    = "localhost:5432"
db_user    = "postgres"
db_password= "postgres"
db_name    = "pos_db"
customer_table = "customers"
internal_table = "internal_users"

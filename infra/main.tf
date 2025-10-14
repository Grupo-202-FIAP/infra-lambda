module "cognito_user_pool_customer" {
  source       = "./modules/cognito_user_pool_customer"
  project_name = var.project_name
  # next_lambda  = module.lambda_sync_customer.lambda_sync_customer_arn
}

module "cognito_user_pool_internal" {
  source       = "./modules/cognito_user_pool_internal"
  project_name = var.project_name
  # next_lambda  = module.lambda_sync_internal.lambda_sync_internal_arn
}

module "lambda_role" {
  source    = "./modules/iam/roles"
  role_name = "LambdaAuthorizerRole"
}

module "lambda_policy" {
  source      = "./modules/iam/policies"
  policy_name = "LambdaAuthorizerPolicy"
  description = "Permissões para Lambda Authorizer"
  policy_document = {
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "cognito-idp:AdminInitiateAuth",
          "cognito-idp:AdminRespondToAuthChallenge",
          "cognito-idp:ListUsers"
        ]
        Resource = "*"
      }
    ]
  }
}


resource "aws_iam_role_policy_attachment" "attach" {
  role       = module.lambda_role.role_name
  policy_arn = module.lambda_policy.policy_arn
}

resource "aws_ecr_repository" "lambda_auth_repo" {
  name                 = "lambda-authorizer-auth-repo"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

locals {
  lambda_auth_image_uri = "${aws_ecr_repository.lambda_auth_repo.repository_url}:${var.lambda_auth_image_tag}"
}


# --- Lambda Authorizer Customer ---
module "lambda_authorizer_customer" {
  source        = "./modules/lambda_auth"
  function_name = var.authorizer_customer_name
  account_id    = var.account_id
  role_arn      = module.lambda_role.role_arn
  package_type  = var.package_type
  timeout       = var.timeout
  memory_size   = var.memory_size
  image_uri     = local.lambda_auth_image_uri

  environment_variables = {
    USER_POOLS = "customer:${module.cognito_user_pool_customer.user_pool_id}"
    REGION     = var.aws_region
    JWT_SECRET = "3"
  }

  depends_on = [aws_ecr_repository.lambda_auth_repo]
}

# --- Lambda Authorizer Internal ---
module "lambda_authorizer_internal" {
  source        = "./modules/lambda_auth"
  function_name = var.authorizer_internal_name
  account_id    = var.account_id
  role_arn      = module.lambda_role.role_arn
  package_type  = var.package_type
  timeout       = var.timeout
  memory_size   = var.memory_size
  image_uri     = local.lambda_auth_image_uri


  environment_variables = {
    USER_POOLS             = "internal:${module.cognito_user_pool_internal.user_pool_id}"
    REGION                 = var.aws_region
    INTERNAL_APP_CLIENT_ID = module.cognito_user_pool_internal.app_client_id
  }

  depends_on = [aws_ecr_repository.lambda_auth_repo]

}






# # --- Lambda Authorizer Customer ---
# module "lambda_authorizer_customer" {
#   source                          = "./modules/lambda_authorizer_customer"
#   authorizer_customer_name        = var.authorizer_customer_name
#   authorizer_customer_handler     = var.authorizer_customer_handler
#   authorizer_customer_output_path = var.authorizer_customer_output_path
#   lambda_runtime                  = var.lambda_runtime
#   lambda_archive_type             = var.lambda_archive_type
#   region                          = var.aws_region
#   account_id                      = var.account_id
#   user_pools = {
#     customer = module.cognito_user_pool_customer.user_pool_id
#   }
# }

# # --- Lambda Authorizer Internal ---
# module "lambda_authorizer_internal" {
#   source                          = "./modules/lambda_authorizer_internal"
#   authorizer_internal_name        = var.authorizer_internal_name
#   authorizer_internal_handler     = var.authorizer_internal_handler
#   authorizer_internal_output_path = var.authorizer_internal_output_path
#   lambda_runtime                  = var.lambda_runtime
#   lambda_archive_type             = var.lambda_archive_type
#   region                          = var.aws_region
#   account_id                      = var.account_id
#   user_pools = {
#     internal = module.cognito_user_pool_internal.user_pool_id
#   }

#   internal_app_client_id = module.cognito_user_pool_internal.app_client_id
# }

# # --- Lambda Registration Customer ---
# module "lambda_registration_customer" {
#   source                            = "./modules/lambda_registration_customer"
#   registration_customer_handler     = var.registration_customer_handler
#   registration_customer_name        = var.registration_customer_name
#   registration_customer_output_path = var.registration_customer_output_path
#   lambda_runtime                    = var.lambda_runtime
#   lambda_archive_type               = var.lambda_archive_type
#   region                            = var.aws_region
#   lambda_source_dir                 = "${path.module}/../src/lambda_registration_customer"
#   account_id                        = var.account_id
#   user_pools = {
#     customer = module.cognito_user_pool_customer.user_pool_id
#   }
# }

# # --- Lambda Registration Internal ---
# module "lambda_registration_internal" {
#   source                            = "./modules/lambda_registration_internal"
#   registration_internal_handler     = var.registration_internal_handler
#   registration_internal_name        = var.registration_internal_name
#   registration_internal_output_path = var.registration_internal_output_path
#   lambda_runtime                    = var.lambda_runtime
#   lambda_archive_type               = var.lambda_archive_type
#   region                            = var.aws_region
#   lambda_source_dir                 = "${path.module}/../src/lambda_registration_internal"
#   account_id                        = var.account_id
#   user_pools = {
#     internal = module.cognito_user_pool_internal.user_pool_id
#   }
#   internal_app_client_id = module.cognito_user_pool_internal.app_client_id
# }

# # --- Lambda Sync Internal ---
# module "lambda_sync_internal" {
#   source                    = "./modules/lambda_sync_internal"
#   sync_internal_handler     = var.sync_internal_handler
#   sync_internal_name        = var.sync_internal_name
#   sync_internal_output_path = var.sync_internal_output_path
#   lambda_runtime            = var.lambda_runtime
#   lambda_archive_type       = var.lambda_archive_type
#   region                    = var.aws_region
#   lambda_source_dir         = "${path.module}/../src/lambda_sync_internal"
#   account_id                = var.account_id
#   subnet_ids                = data.terraform_remote_state.network.outputs.private_subnet_ids
#   security_group_ids        = [data.terraform_remote_state.network.outputs.security_group_postgres_id]
# }

# resource "aws_lambda_permission" "allow_cognito_invoke_internal" {
#   statement_id  = "AllowExecutionFromCognito"
#   action        = "lambda:InvokeFunction"
#   function_name = module.lambda_sync_internal.lambda_sync_internal_name
#   principal     = "cognito-idp.amazonaws.com"
#   source_arn    = module.cognito_user_pool_internal.cognito_internal_arn
# }

# # --- Lambda Sync Customer ---
# module "lambda_sync_customer" {
#   source                    = "./modules/lambda_sync_customer"
#   sync_customer_handler     = var.sync_customer_handler
#   sync_customer_name        = var.sync_customer_name
#   sync_customer_output_path = var.sync_customer_output_path
#   lambda_runtime            = var.lambda_runtime
#   lambda_archive_type       = var.lambda_archive_type
#   region                    = var.aws_region
#   lambda_source_dir         = "${path.module}/../src/lambda_sync_customer"
#   account_id                = var.account_id
#   subnet_ids                = data.terraform_remote_state.network.outputs.private_subnet_ids
#   security_group_ids        = [data.terraform_remote_state.network.outputs.security_group_postgres_id]
# }

# resource "aws_lambda_permission" "allow_cognito_invoke_customer" {
#   statement_id  = "AllowExecutionFromCognito"
#   action        = "lambda:InvokeFunction"
#   function_name = module.lambda_sync_customer.lambda_sync_customer_name
#   principal     = "cognito-idp.amazonaws.com"
#   source_arn    = module.cognito_user_pool_customer.cognito_customer_arn
# }

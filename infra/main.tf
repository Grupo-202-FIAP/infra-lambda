module "cognito_user_pool_customer" {
  source       = "./modules/cognito_user_pool_customer"
  project_name = var.project_name
}

module "cognito_user_pool_internal" {
  source       = "./modules/cognito_user_pool_internal"
  project_name = var.project_name
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

module "lambda_registration_role" {
  source    = "./modules/iam/roles"
  role_name = "LambdaRegistrationRole"
}

module "lambda_registration_policy" {
  source      = "./modules/iam/policies"
  policy_name = "LambdaRegistrationPolicy"
  description = "Permissões para Lambda de Registro de Usuários"
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
          "cognito-idp:AdminCreateUser",
          "cognito-idp:AdminSetUserPassword",
          "cognito-idp:AdminAddUserToGroup",
          "cognito-idp:ListUsers",
          "cognito-idp:AdminUpdateUserAttributes",
          "cognito-idp:AdminGetUser",
          "cognito-idp:AdminInitiateAuth"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "ssm:GetParameter",
          "ssm:GetParameters",
          "ssm:GetParametersByPath"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "ec2:CreateNetworkInterface",
          "ec2:DescribeNetworkInterfaces",
          "ec2:DeleteNetworkInterface"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "sqs:SendMessage",
          "sqs:GetQueueAttributes",
          "sqs:GetQueueUrl"
        ]
        Resource = "*"
      }
    ]
  }
}

resource "aws_iam_role_policy_attachment" "attach_lambda_registration" {
  role       = module.lambda_registration_role.role_name
  policy_arn = module.lambda_registration_policy.policy_arn
}


# IAM role & policy for Lambda Get User
module "lambda_get_user_role" {
  source    = "./modules/iam/roles"
  role_name = "LambdaGetUserRole"
}

module "lambda_get_user_policy" {
  source      = "./modules/iam/policies"
  policy_name = "LambdaGetUserPolicy"
  description = "Permissões para Lambda de busca de usuários"
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
          "ssm:GetParameter",
          "ssm:GetParameters",
          "ssm:GetParametersByPath"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "ec2:CreateNetworkInterface",
          "ec2:DescribeNetworkInterfaces",
          "ec2:DeleteNetworkInterface"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = "*"
      }
    ]
  }
}

resource "aws_iam_role_policy_attachment" "attach_lambda_get_user" {
  role       = module.lambda_get_user_role.role_name
  policy_arn = module.lambda_get_user_policy.policy_arn
}

# IAM role & policy for Lambda List Users
module "lambda_list_users_role" {
  source    = "./modules/iam/roles"
  role_name = "LambdaListUsersRole"
}

module "lambda_list_users_policy" {
  source      = "./modules/iam/policies"
  policy_name = "LambdaListUsersPolicy"
  description = "Permissões para Lambda de listagem de usuários"
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
          "ssm:GetParameter",
          "ssm:GetParameters",
          "ssm:GetParametersByPath"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "ec2:CreateNetworkInterface",
          "ec2:DescribeNetworkInterfaces",
          "ec2:DeleteNetworkInterface"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = "*"
      }
    ]
  }
}

resource "aws_iam_role_policy_attachment" "attach_lambda_list_users" {
  role       = module.lambda_list_users_role.role_name
  policy_arn = module.lambda_list_users_policy.policy_arn
}


resource "aws_ecr_repository" "lambda_auth_repo" {
  name                 = "lambda-authorizer-repo"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "lambda_registration_repo" {
  name                 = "lambda-registration-repo"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "lambda_get_user_repo" {
  name                 = "lambda-get-user-repo"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "lambda_list_users_repo" {
  name                 = "lambda-list-users-repo"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}


# --- Lambda Authorizer  ---
module "lambda_authorizer" {
  source        = "./modules/lambda_auth"
  function_name = var.authorizer_name
  account_id    = var.account_id
  role_arn      = module.lambda_role.role_arn
  package_type  = var.package_type
  timeout       = var.timeout
  memory_size   = var.memory_size
  image_uri     = local.lambda_auth_image_uri

  environment_variables = {
    CUSTOMER_USER_POOL_ID  = module.cognito_user_pool_customer.user_pool_id
    INTERNAL_USER_POOL_ID  = module.cognito_user_pool_internal.user_pool_id
    INTERNAL_APP_CLIENT_ID = module.cognito_user_pool_internal.app_client_id
    REGION                 = var.aws_region
    JWT_SECRET             = "3"
  }

  depends_on = [aws_ecr_repository.lambda_auth_repo]
}

# --- Lambda Registration ---
module "lambda_registration" {
  source        = "./modules/lambda_registration"
  function_name = var.lambda_registration_name
  role_arn      = module.lambda_registration_role.role_arn
  role_name     = module.lambda_registration_role.role_name
  image_uri     = local.lambda_registration_image_uri
  package_type  = var.package_type
  timeout       = var.timeout
  memory_size   = var.memory_size

  environment_variables = {
    CUSTOMER_USER_POOL_ID  = module.cognito_user_pool_customer.user_pool_id
    INTERNAL_USER_POOL_ID  = module.cognito_user_pool_internal.user_pool_id
    INTERNAL_APP_CLIENT_ID = module.cognito_user_pool_internal.app_client_id
    REGION                 = var.aws_region
    DB_HOST                = data.terraform_remote_state.database.outputs.rds_endpoint
    DB_USER                = data.terraform_remote_state.database.outputs.rds_username
    DB_PASSWORD            = data.aws_ssm_parameter.rds_password.value
    DB_NAME                = var.db_name
    CUSTOMER_TABLE         = var.customer_table
    INTERNAL_TABLE         = var.internal_table
  }

  subnet_ids         = data.terraform_remote_state.network.outputs.private_subnet_ids
  security_group_ids = [data.terraform_remote_state.network.outputs.security_group_postgres_id]

  depends_on = [aws_ecr_repository.lambda_registration_repo]
}

# --- Lambda Get User ---
module "lambda_get_user" {
  source        = "./modules/lambda_get_user"
  function_name = var.lambda_get_user_name
  role_arn      = module.lambda_get_user_role.role_arn
  role_name     = module.lambda_get_user_role.role_name
  image_uri     = local.lambda_get_user_image_uri
  package_type  = var.package_type
  timeout       = var.timeout
  memory_size   = var.memory_size

  environment_variables = {
    REGION         = var.aws_region
    DB_HOST        = data.terraform_remote_state.database.outputs.rds_endpoint
    DB_USER        = data.terraform_remote_state.database.outputs.rds_username
    DB_PASSWORD    = data.aws_ssm_parameter.rds_password.value
    DB_NAME        = var.db_name
    CUSTOMER_TABLE = var.customer_table
    INTERNAL_TABLE = var.internal_table
  }

  subnet_ids         = data.terraform_remote_state.network.outputs.private_subnet_ids
  security_group_ids = [data.terraform_remote_state.network.outputs.security_group_postgres_id]

  depends_on = [aws_ecr_repository.lambda_get_user_repo]
}

# --- Lambda List Users ---
module "lambda_list_users" {
  source        = "./modules/lambda_list_users"
  function_name = var.lambda_list_users_name
  role_arn      = module.lambda_list_users_role.role_arn
  role_name     = module.lambda_list_users_role.role_name
  image_uri     = local.lambda_list_users_image_uri
  package_type  = var.package_type
  timeout       = var.timeout
  memory_size   = var.memory_size

  environment_variables = {
    REGION         = var.aws_region
    DB_HOST        = data.terraform_remote_state.database.outputs.rds_endpoint
    DB_USER        = data.terraform_remote_state.database.outputs.rds_username
    DB_PASSWORD    = data.aws_ssm_parameter.rds_password.value
    DB_NAME        = var.db_name
    CUSTOMER_TABLE = var.customer_table
    INTERNAL_TABLE = var.internal_table
  }

  subnet_ids         = data.terraform_remote_state.network.outputs.private_subnet_ids
  security_group_ids = [data.terraform_remote_state.network.outputs.security_group_postgres_id]

  depends_on = [aws_ecr_repository.lambda_list_users_repo]
}

# --- Lambda Permissions para Cognito ---
resource "aws_lambda_permission" "allow_cognito_invoke_internal" {
  statement_id  = "AllowExecutionFromCognitoInternal"
  action        = "lambda:InvokeFunction"
  function_name = module.lambda_registration.arn
  principal     = "cognito-idp.amazonaws.com"
  source_arn    = module.cognito_user_pool_internal.cognito_internal_arn

  depends_on = [module.lambda_registration]
}

resource "aws_lambda_permission" "allow_cognito_invoke_customer" {
  statement_id  = "AllowExecutionFromCognitoCustomer"
  action        = "lambda:InvokeFunction"
  function_name = module.lambda_registration.arn
  principal     = "cognito-idp.amazonaws.com"
  source_arn    = module.cognito_user_pool_customer.cognito_customer_arn

  depends_on = [module.lambda_registration]
}

# --- Atualização dos triggers do Cognito ---
resource "null_resource" "cognito_customer_trigger" {
  provisioner "local-exec" {
    command = "aws cognito-idp update-user-pool --user-pool-id ${module.cognito_user_pool_customer.user_pool_id} --lambda-config PreSignUp=${module.lambda_registration.arn} --region us-east-1"
  }

  depends_on = [module.lambda_registration]
}

resource "null_resource" "cognito_internal_trigger" {
  provisioner "local-exec" {
    command = "aws cognito-idp update-user-pool --user-pool-id ${module.cognito_user_pool_internal.user_pool_id} --lambda-config PreSignUp=${module.lambda_registration.arn} --region us-east-1"
  }

  depends_on = [module.lambda_registration]
}




resource "aws_lambda_function" "lambda_authorizer" {
  function_name = var.function_name
  role          = var.role_arn
  image_uri     = "234411838279.dkr.ecr.us-east-1.amazonaws.com/lambda-authorizer-repo@sha256:fb4cae0997558a1eb9a0a4cf7b29242f33b43e36a9fc02873f6659a645d047de"
  package_type  = var.package_type
  timeout       = var.timeout
  memory_size   = var.memory_size


  environment {
    variables = var.environment_variables
  }
}
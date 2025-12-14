
resource "aws_lambda_function" "lambda_authorizer" {
  function_name = var.function_name
  role          = var.role_arn
  image_uri     = var.image_uri
  package_type  = var.package_type
  timeout       = var.timeout
  memory_size   = var.memory_size


  environment {
    variables = var.environment_variables
  }
}
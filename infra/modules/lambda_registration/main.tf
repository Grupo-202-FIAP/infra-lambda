resource "aws_lambda_function" "lambda_registration" {
  function_name = var.function_name
  role          = var.role_arn
  package_type  = var.package_type
  image_uri     = var.image_uri

  memory_size   = var.memory_size
  timeout       = var.timeout

  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = var.security_group_ids
  }

  environment {
    variables = var.environment_variables
  }
}

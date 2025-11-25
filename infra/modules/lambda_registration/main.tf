resource "aws_lambda_function" "lambda_registration" {
  function_name = var.function_name
  role          = var.role_arn
  package_type  = var.package_type
  image_uri     = "234411838279.dkr.ecr.us-east-1.amazonaws.com/lambda-registration-repo@sha256:cfdf87ce5cc30875c61e939075130b7f7009c3b9969467c9f952663233e33e18"

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

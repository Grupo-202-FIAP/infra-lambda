data "archive_file" "lambda_authorizer_customer_zip" {
  type        = var.lambda_archive_type
  source_dir  = "${path.module}/../../../src/lambda_authorizer_customer"
  output_path = var.authorizer_customer_output_path
}

resource "aws_lambda_function" "lambda_authorizer_customer" {
  function_name    = var.authorizer_customer_name
  handler          = var.authorizer_customer_handler
  runtime          = var.lambda_runtime
  role             = "arn:aws:iam::${var.account_id}:role/LabRole"
  filename         = data.archive_file.lambda_authorizer_customer_zip.output_path
  source_code_hash = data.archive_file.lambda_authorizer_customer_zip.output_base64sha256

  environment {
    variables = {
      USER_POOLS = "customer:${var.user_pools["customer"]}"
      REGION     = var.region
    }
  }
}

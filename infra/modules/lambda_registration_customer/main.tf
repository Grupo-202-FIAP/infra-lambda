data "archive_file" "lambda_registration_customer_zip" {
  type        = var.lambda_archive_type
  source_dir  = var.lambda_source_dir
  output_path = var.registration_customer_output_path
}

resource "aws_lambda_function" "lambda_registration_customer" {
  function_name = var.registration_customer_name
  handler       = var.registration_customer_handler
  runtime       = var.lambda_runtime
  role          = "arn:aws:iam::${var.account_id}:role/LabRole"

  filename         = data.archive_file.lambda_registration_customer_zip.output_path
  source_code_hash = data.archive_file.lambda_registration_customer_zip.output_base64sha256

  memory_size = var.lambda_memory_size
  timeout     = var.lambda_timeout

  environment {
    variables = {
      USER_POOL_ID = var.user_pools["customer"]
      REGION       = var.region
    }
  }
}

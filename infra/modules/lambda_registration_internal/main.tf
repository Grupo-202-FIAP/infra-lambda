data "archive_file" "lambda_registration_internal_zip" {
  type        = var.lambda_archive_type
  source_dir  = var.lambda_source_dir
  output_path = var.registration_internal_output_path
}

resource "aws_lambda_function" "lambda_registration_internal" {
  function_name = var.registration_internal_name
  handler       = var.registration_internal_handler
  runtime       = var.lambda_runtime
  role          = "arn:aws:iam::${var.account_id}:role/LabRole"

  filename         = data.archive_file.lambda_registration_internal_zip.output_path
  source_code_hash = data.archive_file.lambda_registration_internal_zip.output_base64sha256

  memory_size = var.lambda_memory_size
  timeout     = var.lambda_timeout

  environment {
    variables = {
      USER_POOL_ID           = var.user_pools["internal"]
      INTERNAL_APP_CLIENT_ID = var.internal_app_client_id
      REGION                 = var.region
    }
  }
}

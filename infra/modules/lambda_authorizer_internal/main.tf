data "archive_file" "lambda_authorizer_internal_zip" {
  type        = var.lambda_archive_type
  source_dir  = "${path.module}/../../../src/lambda_authorizer_internal"
  output_path = var.authorizer_internal_output_path
}

resource "aws_lambda_function" "lambda_authorizer_internal" {
  function_name    = var.authorizer_internal_name
  handler          = var.authorizer_internal_handler
  runtime          = var.lambda_runtime
  role             = "arn:aws:iam::${var.account_id}:role/LabRole"
  filename         = data.archive_file.lambda_authorizer_internal_zip.output_path
  source_code_hash = data.archive_file.lambda_authorizer_internal_zip.output_base64sha256

  environment {
    variables = {
      USER_POOLS             = "internal:${var.user_pools["internal"]}"
      REGION                 = var.region
      INTERNAL_APP_CLIENT_ID = var.internal_app_client_id
    }
  }
}

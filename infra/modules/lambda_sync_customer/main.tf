data "archive_file" "lambda_sync_customer_zip" {
  type        = var.lambda_archive_type
  source_dir  = var.lambda_source_dir
  output_path = var.sync_customer_output_path
}

resource "aws_lambda_function" "lambda_sync_customer" {
  function_name = var.sync_customer_name
  handler       = var.sync_customer_handler
  runtime       = var.lambda_runtime
  role          = "arn:aws:iam::${var.account_id}:role/LabRole"

  filename         = data.archive_file.lambda_sync_customer_zip.output_path
  source_code_hash = data.archive_file.lambda_sync_customer_zip.output_base64sha256

  memory_size = var.lambda_memory_size
  timeout     = var.lambda_timeout

  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = var.security_group_ids
  }

}

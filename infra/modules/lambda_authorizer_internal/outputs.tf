output "lambda_authorizer_internal_name" {
  description = "O nome da função Lambda Authorizer (internal)."
  value       = aws_lambda_function.lambda_authorizer_internal.function_name
}

output "lambda_authorizer_internal_invoke_arn" {
  description = "O ARN da função Lambda Authorizer (internal)."
  value       = aws_lambda_function.lambda_authorizer_internal.invoke_arn
}

output "lambda_registration_internal_name" {
  description = "Nome da Lambda Registration Internal"
  value       = aws_lambda_function.lambda_registration_internal.function_name
}

output "lambda_registration_internal_invoke_arn" {
  description = "ARN para invocação da Lambda Registration Internal"
  value       = aws_lambda_function.lambda_registration_internal.invoke_arn
}

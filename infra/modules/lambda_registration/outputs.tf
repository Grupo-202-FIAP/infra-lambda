output "function_name" {
  description = "Nome da Lambda Registration"
  value       = aws_lambda_function.lambda_registration.function_name
}

output "invoke_arn" {
  description = "ARN para invocação via API Gateway"
  value       = aws_lambda_function.lambda_registration.invoke_arn
}

output "arn" {
  description = "ARN completo da Lambda Registration"
  value       = aws_lambda_function.lambda_registration.arn
}

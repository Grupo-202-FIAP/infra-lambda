output "function_name" {
  description = "Nome da Lambda List Users"
  value       = aws_lambda_function.lambda_list_users.function_name
}

output "invoke_arn" {
  description = "ARN para invocação via API Gateway"
  value       = aws_lambda_function.lambda_list_users.invoke_arn
}

output "arn" {
  description = "ARN completo da Lambda List Users"
  value       = aws_lambda_function.lambda_list_users.arn
}

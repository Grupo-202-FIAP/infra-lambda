output "function_name" {
  description = "Nome da Lambda Get User"
  value       = aws_lambda_function.lambda_get_user.function_name
}

output "invoke_arn" {
  description = "ARN para invocação via API Gateway"
  value       = aws_lambda_function.lambda_get_user.invoke_arn
}

output "arn" {
  description = "ARN completo da Lambda Get User"
  value       = aws_lambda_function.lambda_get_user.arn
}

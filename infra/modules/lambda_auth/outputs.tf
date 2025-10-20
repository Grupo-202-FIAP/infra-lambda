output "function_name" {
  description = "Nome da Lambda Authorizer"
  value       = aws_lambda_function.lambda_authorizer.function_name
}

output "invoke_arn" {
  description = "ARN para invocação via API Gateway"
  value       = aws_lambda_function.lambda_authorizer.invoke_arn
}

output "arn" {
  description = "ARN completo da Lambda Authorizer"
  value       = aws_lambda_function.lambda_authorizer.arn
}

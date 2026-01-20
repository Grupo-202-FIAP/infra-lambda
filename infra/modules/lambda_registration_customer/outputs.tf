output "lambda_registration_customer_name" {
  description = "Nome da Lambda Registration Customer"
  value       = aws_lambda_function.lambda_registration_customer.function_name
}

output "lambda_registration_customer_invoke_arn" {
  description = "ARN para invocação da Lambda Registration Customer"
  value       = aws_lambda_function.lambda_registration_customer.invoke_arn
}

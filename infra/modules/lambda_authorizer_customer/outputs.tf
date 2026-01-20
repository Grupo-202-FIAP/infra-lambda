output "lambda_authorizer_customer_name" {
  description = "O nome da função Lambda Authorizer (customer)."
  value       = aws_lambda_function.lambda_authorizer_customer.function_name
}

output "lambda_authorizer_customer_invoke_arn" {
  description = "O ARN da função Lambda Authorizer (customer)."
  value       = aws_lambda_function.lambda_authorizer_customer.invoke_arn
}


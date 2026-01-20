output "user_pool_id" {
  value = aws_cognito_user_pool.customer.id
}

output "cognito_customer_arn" {
  description = "ARN para invocação da Lambda Sync Customer"
  value       = aws_cognito_user_pool.customer.arn
}

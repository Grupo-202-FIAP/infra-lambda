output "user_pool_id" {
  value = aws_cognito_user_pool.internal.id
}

output "app_client_id" {
  value = aws_cognito_user_pool_client.internal.id
}

output "cognito_internal_arn" {
  description = "ARN para invocação da Lambda Sync Internal"
  value       = aws_cognito_user_pool.internal.arn
}
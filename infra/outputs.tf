output "ecr_repository_url" {
  description = "URL do ECR para fazer o docker push da imagem Lambda Authorizer"
  value       = aws_ecr_repository.lambda_auth_repo.repository_url
}

output "lambda_authorizer_function_name" {
  value = module.lambda_authorizer.function_name
}

output "lambda_authorizer_invoke_arn" {
  value = module.lambda_authorizer.invoke_arn
}

output "lambda_authorizer_arn" {
  value = module.lambda_authorizer.arn
}

output "lambda_registration_function_name" {
  value = module.lambda_registration.function_name
}

output "lambda_registration_invoke_arn" {
  value = module.lambda_registration.invoke_arn
}

output "lambda_registration_arn" {
  value = module.lambda_registration.arn
}

output "lambda_get_user_function_name" {
  value = module.lambda_get_user.function_name
}

output "lambda_get_user_invoke_arn" {
  value = module.lambda_get_user.invoke_arn
}

output "lambda_get_user_arn" {
  value = module.lambda_get_user.arn
}

output "lambda_list_users_function_name" {
  value = module.lambda_list_users.function_name
}

output "lambda_list_users_invoke_arn" {
  value = module.lambda_list_users.invoke_arn
}

output "lambda_list_users_arn" {
  value = module.lambda_list_users.arn
}

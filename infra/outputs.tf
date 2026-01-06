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

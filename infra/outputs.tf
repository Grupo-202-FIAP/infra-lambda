output "ecr_repository_url" {
  description = "URL do ECR para fazer o docker push da imagem Lambda Authorizer"
  value       = aws_ecr_repository.lambda_auth_repo.repository_url
}
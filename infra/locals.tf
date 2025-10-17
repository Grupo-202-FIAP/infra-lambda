locals {
  lambda_auth_image_uri = "${aws_ecr_repository.lambda_auth_repo.repository_url}:${var.lambda_image_tag}"
}

locals {
  lambda_registration_image_uri = "${aws_ecr_repository.lambda_registration_repo.repository_url}:${var.lambda_image_tag}"
}
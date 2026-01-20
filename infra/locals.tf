locals {
  lambda_auth_image_uri = "${aws_ecr_repository.lambda_auth_repo.repository_url}:${var.lambda_image_tag}"
}

locals {
  lambda_registration_image_uri = "${aws_ecr_repository.lambda_registration_repo.repository_url}:${var.lambda_image_tag}"
}

locals {
  lambda_get_user_image_uri = "${aws_ecr_repository.lambda_get_user_repo.repository_url}:${var.lambda_image_tag}"
}

locals {
  lambda_list_users_image_uri = "${aws_ecr_repository.lambda_list_users_repo.repository_url}:${var.lambda_image_tag}"
}
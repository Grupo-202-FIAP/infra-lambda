data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    bucket = "terraform-state-bucket-nextime"
    key    = "infra.tfstate"
    region = "us-east-1"
  }
}

data "aws_ssm_parameter" "db_user" {
  name = "/fastfood/rds/username"
}

data "aws_ssm_parameter" "db_password" {
  name = "/fastfood/rds/password"
  with_decryption = true
}
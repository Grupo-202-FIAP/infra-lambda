data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    bucket = "nextime-food-state-bucket"
    key    = "infra-core/infra.tfstate"
    region = "us-east-1"
  }
}

data "terraform_remote_state" "database" {
  backend = "s3"
  config = {
    bucket = "nextime-food-state-bucket"
    key    = "infra-database/infra.tfstate"
    region = "us-east-1"
  }
}

data "aws_ssm_parameter" "rds_password" {
  name            = data.terraform_remote_state.database.outputs.rds_password_ssm_param
  with_decryption = true
}
terraform {
  backend "s3" {
    bucket = "yolo-on-aws-terraform-state"
    key    = "global/s3/terraform.tfstate"
    region = "us-east-1"
  }
}

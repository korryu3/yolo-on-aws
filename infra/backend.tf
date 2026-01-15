terraform {
  backend "s3" {
    bucket = "yolo-on-aws-tf-state"
    key    = "global/s3/terraform.tfstate"
    region = "us-east-1"
  }
}

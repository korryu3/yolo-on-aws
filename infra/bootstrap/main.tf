terraform {
  required_version = ">= 1.13.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Terraform state用のS3バケット
resource "aws_s3_bucket" "terraform_state" {
  bucket = "yolo-on-aws-terraform-state"

  tags = {
    Name        = "Terraform State Bucket"
    Environment = "Infrastructure"
    ManagedBy   = "Terraform"
  }
}

# バケットバージョニングの有効化
resource "aws_s3_bucket_versioning" "terraform_state_versioning" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

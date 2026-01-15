variable "aws_region" {
  description = "The AWS region to deploy resources in"
  type        = string
  default     = "us-east-1"
}

variable "image_uri" {
  description = "ECRのイメージURI. bash api-push.shの出力を指定する"
}

variable "execution_role_arn" {
  description = "ECSタスク実行用のIAMロールARN. LabRoleのARNを指定する"
}

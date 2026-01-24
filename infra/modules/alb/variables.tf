variable "name_prefix" {
  description = "リソース名のプレフィックス"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "subnet_ids" {
  description = "ALBを配置するサブネットID"
  type        = list(string)
}

variable "security_group_id" {
  description = "ALB用セキュリティグループID"
  type        = string
}

variable "target_port" {
  description = "ターゲットグループのポート"
  type        = number
  default     = 8080
}

variable "health_check_path" {
  description = "ヘルスチェックのパス"
  type        = string
  default     = "/healthz"
}

variable "name_prefix" {
  description = "リソース名のプレフィックス"
  type        = string
}

variable "aws_region" {
  description = "AWSリージョン"
  type        = string
}

variable "image_uri" {
  description = "コンテナイメージURI"
  type        = string
}

variable "execution_role_arn" {
  description = "ECSタスク実行ロールARN"
  type        = string
}

variable "cpu" {
  description = "タスクのCPU（vCPU単位）"
  type        = number
  default     = 256
}

variable "memory" {
  description = "タスクのメモリ（MB）"
  type        = number
  default     = 512
}

variable "container_port" {
  description = "コンテナのポート"
  type        = number
  default     = 8080
}

variable "desired_count" {
  description = "希望タスク数"
  type        = number
  default     = 1
}

variable "subnet_ids" {
  description = "ECSタスクを配置するサブネットID"
  type        = list(string)
}

variable "security_group_id" {
  description = "ECSタスク用セキュリティグループID"
  type        = string
}

variable "target_group_arn" {
  description = "ALBターゲットグループARN"
  type        = string
}

variable "alb_listener_arn" {
  description = "ALBリスナーARN（依存関係用）"
  type        = string
}

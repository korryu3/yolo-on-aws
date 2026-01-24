# ======================
# 必須変数
# ======================
variable "image_uri" {
  description = "ECRのイメージURI. bash api-push.shの出力を指定する"
  type        = string
}

variable "execution_role_arn" {
  description = "ECSタスク実行用のIAMロールARN. LabRoleのARNを指定する"
  type        = string
}

# ======================
# 環境設定
# ======================
variable "environment" {
  description = "デプロイ環境（dev, staging, prod）"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment は dev, staging, prod のいずれかである必要があります"
  }
}

variable "aws_region" {
  description = "AWSリージョン"
  type        = string
  default     = "us-east-1"
}

# ======================
# ネットワーク設定
# ======================
variable "vpc_cidr" {
  description = "VPCのCIDRブロック"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "パブリックサブネットのCIDRブロック"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "availability_zones" {
  description = "使用するAZ（空の場合はリージョンの最初の2つを使用）"
  type        = list(string)
  default     = []
}

# ======================
# ECR設定
# ======================
variable "enable_force_delete" {
  description = "ECRリポジトリの強制削除を許可するか（開発環境用）"
  type        = bool
  default     = false
}

# ======================
# ECS設定
# ======================
variable "ecs_task_cpu" {
  description = "ECSタスクのCPU（vCPU単位、256 = 0.25 vCPU）"
  type        = number
  default     = 256
}

variable "ecs_task_memory" {
  description = "ECSタスクのメモリ（MB単位）"
  type        = number
  default     = 512
}

variable "ecs_desired_count" {
  description = "ECSサービスの希望タスク数"
  type        = number
  default     = 1
}

variable "container_port" {
  description = "コンテナのポート番号"
  type        = number
  default     = 8080
}

# ======================
# 共通設定
# ======================
variable "project_name" {
  description = "プロジェクト名（リソース名のプレフィックスに使用）"
  type        = string
  default     = "yolo-on-aws"
}

# ======================
# 共通タグ定義
# ======================
locals {
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }

  # AZの計算（指定がなければリージョンの最初の2つを使用）
  availability_zones = length(var.availability_zones) > 0 ? var.availability_zones : [
    "${var.aws_region}a",
    "${var.aws_region}b"
  ]

  # リソース名のプレフィックス
  name_prefix = var.project_name
}

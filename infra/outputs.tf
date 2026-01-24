# ======================
# ALB Outputs
# ======================
output "alb_dns_name" {
  description = "ALBのURL（ブラウザでアクセスできる）"
  value       = "http://${module.alb.dns_name}"
}

output "alb_arn" {
  description = "ALBのARN"
  value       = module.alb.arn
}

# ======================
# ECS Outputs
# ======================
output "ecs_cluster_name" {
  description = "ECSクラスター名"
  value       = module.ecs.cluster_name
}

output "ecs_service_name" {
  description = "ECSサービス名"
  value       = module.ecs.service_name
}

# ======================
# ECR Outputs
# ======================
output "ecr_repository_url" {
  description = "ECRリポジトリURL"
  value       = module.ecr.repository_url
}

# ======================
# Networking Outputs
# ======================
output "vpc_id" {
  description = "VPC ID"
  value       = module.networking.vpc_id
}

output "public_subnet_ids" {
  description = "パブリックサブネットのID"
  value       = module.networking.public_subnet_ids
}

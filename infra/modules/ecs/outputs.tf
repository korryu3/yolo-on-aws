output "cluster_id" {
  description = "ECSクラスターID"
  value       = aws_ecs_cluster.main.id
}

output "cluster_name" {
  description = "ECSクラスター名"
  value       = aws_ecs_cluster.main.name
}

output "service_name" {
  description = "ECSサービス名"
  value       = aws_ecs_service.api.name
}

output "task_definition_arn" {
  description = "タスク定義ARN"
  value       = aws_ecs_task_definition.api.arn
}

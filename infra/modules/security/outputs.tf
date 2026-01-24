output "alb_security_group_id" {
  description = "ALB用セキュリティグループID"
  value       = aws_security_group.alb.id
}

output "ecs_task_security_group_id" {
  description = "ECSタスク用セキュリティグループID"
  value       = aws_security_group.ecs_task.id
}

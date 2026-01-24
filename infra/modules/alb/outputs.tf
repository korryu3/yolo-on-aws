output "arn" {
  description = "ALBのARN"
  value       = aws_lb.main.arn
}

output "dns_name" {
  description = "ALBのDNS名"
  value       = aws_lb.main.dns_name
}

output "target_group_arn" {
  description = "ターゲットグループのARN"
  value       = aws_lb_target_group.app.arn
}

output "listener_arn" {
  description = "リスナーのARN"
  value       = aws_lb_listener.http.arn
}

output "repository_url" {
  description = "ECRリポジトリURL"
  value       = aws_ecr_repository.api.repository_url
}

output "repository_arn" {
  description = "ECRリポジトリARN"
  value       = aws_ecr_repository.api.arn
}

output "repository_name" {
  description = "ECRリポジトリ名"
  value       = aws_ecr_repository.api.name
}

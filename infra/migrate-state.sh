#!/bin/bash
# ======================
# Terraform State Migration Script
# ======================
# モジュール化に伴うState移行スクリプト
#
# 使用方法:
#   cd infra
#   bash migrate-state.sh
#
# 注意:
# - 実行前に terraform init を実行してください
# - 本番環境では必ずバックアップを確認してください

set -e

echo "=== Terraform State Migration ==="
echo ""

# Step 1: バックアップ
echo "Step 1: State バックアップ作成..."
terraform state pull > terraform.tfstate.backup.$(date +%Y%m%d_%H%M%S).json
echo "バックアップ完了"
echo ""

# Step 2: Networking モジュールへの移行
echo "Step 2: Networking リソースの移行..."
terraform state mv aws_vpc.main module.networking.aws_vpc.main 2>/dev/null || echo "  - aws_vpc.main: スキップ（既に移行済み or 存在しない）"
terraform state mv aws_internet_gateway.main module.networking.aws_internet_gateway.main 2>/dev/null || echo "  - aws_internet_gateway.main: スキップ"
terraform state mv aws_route_table.public module.networking.aws_route_table.public 2>/dev/null || echo "  - aws_route_table.public: スキップ"

# サブネットは count を使用しているため、インデックス変換が必要
terraform state mv 'aws_subnet.public_1' 'module.networking.aws_subnet.public[0]' 2>/dev/null || echo "  - aws_subnet.public_1: スキップ"
terraform state mv 'aws_subnet.public_2' 'module.networking.aws_subnet.public[1]' 2>/dev/null || echo "  - aws_subnet.public_2: スキップ"
terraform state mv 'aws_route_table_association.public_1' 'module.networking.aws_route_table_association.public[0]' 2>/dev/null || echo "  - aws_route_table_association.public_1: スキップ"
terraform state mv 'aws_route_table_association.public_2' 'module.networking.aws_route_table_association.public[1]' 2>/dev/null || echo "  - aws_route_table_association.public_2: スキップ"
echo ""

# Step 3: Security モジュールへの移行
echo "Step 3: Security リソースの移行..."
terraform state mv aws_security_group.alb module.security.aws_security_group.alb 2>/dev/null || echo "  - aws_security_group.alb: スキップ"
terraform state mv aws_security_group.ecs_task module.security.aws_security_group.ecs_task 2>/dev/null || echo "  - aws_security_group.ecs_task: スキップ"
echo ""

# Step 4: ALB モジュールへの移行
echo "Step 4: ALB リソースの移行..."
terraform state mv aws_lb.main module.alb.aws_lb.main 2>/dev/null || echo "  - aws_lb.main: スキップ"
terraform state mv aws_lb_target_group.app module.alb.aws_lb_target_group.app 2>/dev/null || echo "  - aws_lb_target_group.app: スキップ"
terraform state mv aws_lb_listener.http module.alb.aws_lb_listener.http 2>/dev/null || echo "  - aws_lb_listener.http: スキップ"
echo ""

# Step 5: ECS モジュールへの移行
echo "Step 5: ECS リソースの移行..."
terraform state mv aws_ecs_cluster.main module.ecs.aws_ecs_cluster.main 2>/dev/null || echo "  - aws_ecs_cluster.main: スキップ"
terraform state mv aws_ecs_task_definition.api module.ecs.aws_ecs_task_definition.api 2>/dev/null || echo "  - aws_ecs_task_definition.api: スキップ"
terraform state mv aws_ecs_service.api module.ecs.aws_ecs_service.api 2>/dev/null || echo "  - aws_ecs_service.api: スキップ"
echo ""

# Step 6: ECR モジュールへの移行
echo "Step 6: ECR リソースの移行..."
terraform state mv aws_ecr_repository.api module.ecr.aws_ecr_repository.api 2>/dev/null || echo "  - aws_ecr_repository.api: スキップ"
echo ""

echo "=== State 移行完了 ==="
echo ""
echo "次のステップ:"
echo "  1. terraform plan -var-file=\"dev.tfvars\" で差分を確認"
echo "  2. 「No changes」と表示されれば成功"
echo "  3. 差分がある場合はモジュール内のリソース名を調整"

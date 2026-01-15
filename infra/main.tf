terraform {
  required_version = ">= 1.13.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# ======================
# VPC (Virtual Private Cloud)
# ======================
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true  # VPC内のインスタンスにDNSホスト名を割り当てる（ECSで必要）
  enable_dns_support   = true  # DNS解決を有効化

  tags = {
    Name = "yolo-on-aws-vpc"
  }
}

# ======================
# Internet Gateway
# ======================
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "yolo-on-aws-igw"
  }
}

# ======================
# Public Subnet
# ======================
resource "aws_subnet" "public_1" {
  vpc_id = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "${var.aws_region}a"
  map_public_ip_on_launch = true
}

resource "aws_subnet" "public_2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true

  tags = {
    Name = "yolo-on-aws-public-subnet-2"
  }
}

# ======================
# Public Route Table
# ======================
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "yolo-on-aws-public-rt"
  }
}

# SubnetがPublic Route Tableを使うように関連付け
resource "aws_route_table_association" "public_1" {
  subnet_id      = aws_subnet.public_1.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public_2" {
  subnet_id      = aws_subnet.public_2.id
  route_table_id = aws_route_table.public.id
}

# ======================
# Security Groups (セキュリティグループ)
# ======================
# セキュリティグループは何も書かないと、基本的に拒否される
# 暗黙的なDenyルールがあると考えると良い

# ALB用のセキュリティグループ
resource "aws_security_group" "alb" {
  name = "yolo-on-aws-alb-sg"
  description = "Security group for ALB"
  vpc_id = aws_vpc.main.id

  # 中に入ってくる通信を許可するルール
  # HTTP (ポート80) を全てのIPアドレスから許可
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # 全てのIPアドレスから許可
    description = "Allow HTTP traffic from anywhere"
  }

  # 外部に出て行く通信を許可するルール
  # 全ての通信を許可
  egress {
    from_port = 0
    to_port   = 0
    protocol = "-1" # -1は全てのプロトコルを意味する
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = {
    Name = "yolo-on-aws-alb-sg"
  }
}

# ECSタスク用のセキュリティグループ
resource "aws_security_group" "ecs_task" {
  name = "yolo-on-aws-ecs-task-sg"
  description = "Security group for ECS tasks"
  vpc_id = aws_vpc.main.id

  # インバウンドルール: ALBからのHTTPトラフィックを許可
  ingress {
    from_port = 8080  # Dockerfileで指定したアプリケーションのポート
    to_port   = 8080
    protocol  = "tcp"
    security_groups = [aws_security_group.alb.id] # ALBからだけ許可
    description = "Allow HTTP traffic from ALB"
  }

  # アウトバウンドルール: 全ての通信を許可
  # ECSがECRからイメージをプルするために必要
  egress {
    from_port = 0
    to_port   = 0
    protocol  = "-1" # -1は全てのプロトコルを意味する
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = {
    Name = "yolo-on-aws-ecs-task-sg"
  }
}

# ======================
# Application Load Balancer (ALB)
# ======================

# ALB本体
resource "aws_lb" "main" {
  name = "yolo-on-aws-alb"
  internal = false  # インターネット向けに公開する
  load_balancer_type = "application"
  security_groups = [aws_security_group.alb.id]
  subnets = [
    aws_subnet.public_1.id,
    aws_subnet.public_2.id
  ]

  tags = {
    Name = "yolo-on-aws-alb"
  }
}

# ALBがリクエストをどこに転送するか
resource "aws_lb_target_group" "app" {
  name = "yolo-on-aws-tg"
  port = 8080  # ECSタスクのポートと一致させる
  protocol = "HTTP"
  vpc_id = aws_vpc.main.id
  target_type = "ip"  # FARGATEではipを指定する

  health_check {
    enabled = true
    path = "/healthz"
    port = "traffic-port"
    protocol = "HTTP"
    interval = 30  # ヘルスチェックの間隔（秒）
    timeout = 5    # タイムアウト時間（秒）
    healthy_threshold = 2  # 2回成功したら正常
    unhealthy_threshold = 2  # 2回失敗したら異常
    matcher = "200-399"  # 200番台と300番台を正常とみなす
  }

  tags = {
    Name = "yolo-on-aws-tg"
  }
}

# ALBがどのポートでリクエストを受け付けるか
# 待ち受けるリスナー
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port = 80  # ブラウザからはHTTPの80番ポートでアクセスされる
  protocol = "HTTP"

  # デフォルトで、ターゲットグループに転送する
  default_action {
    type = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}

# ======================
# ECR Cluster
# ======================
resource "aws_ecs_cluster" "main" {
  name = "yolo-on-aws-ecs-cluster"

  tags = {
    Name = "yolo-on-aws-ecs-cluster"
  }
}

# ======================
# ECS Task Definition
# ======================
resource "aws_ecs_task_definition" "api" {
  family = "yolo-on-aws-api-task"
  network_mode = "awsvpc"  # FARGATEではawsvpcを指定する
  requires_compatibilities = ["FARGATE"]
  cpu = "256"               # 0.25 vCPU
  memory = "512"            # 0.5 GB
  execution_role_arn = var.execution_role_arn

  # コンテナの定義
  container_definitions = jsonencode([
    {
      name = "api-container"
      image = var.image_uri
      essential = true  # コンテナが停止したら、タスク全体も停止する

      portMappings = [
        {
          containerPort = 8080  # コンテナ内のポート
          hostPort      = 8080  # ホストのポート（FARGATEでは同じにする必要がある）
          protocol      = "tcp"
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/yolo-on-aws-api"
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs"
          "awslogs-create-group"  = "true"  # ロググループが存在しない場合に作成する
        }
      }
    }
  ])
  tags = {
    Name = "yolo-on-aws-api-task"
  }
}

# ======================
# ECS Service
# ======================
# タスクの常時実行
resource "aws_ecs_service" "api" {
  name = "yolo-on-aws-api-service"
  cluster = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.api.arn
  desired_count = 1  # 同時に実行するタスクの数
  launch_type = "FARGATE"

  # Network設定
  network_configuration {
    subnets = [
      aws_subnet.public_1.id,
      aws_subnet.public_2.id
    ]
    security_groups = [aws_security_group.ecs_task.id]
    assign_public_ip = true  # Public Subnetを使う場合はtrueにする
  }

  # ALBと連携する設定
  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "api-container"
    container_port   = 8080

  }

  # terraformのリソース作成時に、ALBリスナーが作成されてからECSサービスを作成するようにする
  depends_on = [ aws_lb_listener.http ]

  tags = {
    Name = "yolo-on-aws-api-service"
  }
}

# ======================
# Outputs (デプロイ後に表示される情報)
# ======================
output "alb_dns_name" {
  description = "ALBのURL (ブラウザでアクセスできる)"
  value       = "http://${aws_lb.main.dns_name}"
}

output "ecs_cluster_name" {
  description = "ECSクラスター名"
  value       = aws_ecs_cluster.main.name
}

output "ecs_service_name" {
  description = "ECSサービス名"
  value       = aws_ecs_service.api.name
}

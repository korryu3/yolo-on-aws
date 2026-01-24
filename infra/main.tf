# ======================
# Networking Module
# ======================
module "networking" {
  source = "./modules/networking"

  name_prefix         = local.name_prefix
  vpc_cidr            = var.vpc_cidr
  public_subnet_cidrs = var.public_subnet_cidrs
  availability_zones  = local.availability_zones
}

# ======================
# Security Module
# ======================
module "security" {
  source = "./modules/security"

  name_prefix    = local.name_prefix
  vpc_id         = module.networking.vpc_id
  container_port = var.container_port
}

# ======================
# ECR Module
# ======================
module "ecr" {
  source = "./modules/ecr"

  name_prefix  = local.name_prefix
  force_delete = var.enable_force_delete
}

# ======================
# ALB Module
# ======================
module "alb" {
  source = "./modules/alb"

  name_prefix       = local.name_prefix
  vpc_id            = module.networking.vpc_id
  subnet_ids        = module.networking.public_subnet_ids
  security_group_id = module.security.alb_security_group_id
  target_port       = var.container_port
}

# ======================
# ECS Module
# ======================
module "ecs" {
  source = "./modules/ecs"

  name_prefix        = local.name_prefix
  aws_region         = var.aws_region
  image_uri          = var.image_uri
  execution_role_arn = var.execution_role_arn
  cpu                = var.ecs_task_cpu
  memory             = var.ecs_task_memory
  container_port     = var.container_port
  desired_count      = var.ecs_desired_count
  subnet_ids         = module.networking.public_subnet_ids
  security_group_id  = module.security.ecs_task_security_group_id
  target_group_arn   = module.alb.target_group_arn
  alb_listener_arn   = module.alb.listener_arn
}

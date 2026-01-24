variable "name_prefix" {
  description = "リソース名のプレフィックス"
  type        = string
}

variable "vpc_cidr" {
  description = "VPCのCIDRブロック"
  type        = string
}

variable "public_subnet_cidrs" {
  description = "パブリックサブネットのCIDRブロック"
  type        = list(string)
}

variable "availability_zones" {
  description = "使用するAZ"
  type        = list(string)
}

variable "name_prefix" {
  description = "リソース名のプレフィックス"
  type        = string
}

variable "force_delete" {
  description = "イメージがある場合でも強制削除を許可するか"
  type        = bool
  default     = false
}

variable "image_tag_mutability" {
  description = "イメージタグの変更を許可するか"
  type        = string
  default     = "MUTABLE"
}

variable "scan_on_push" {
  description = "プッシュ時にスキャンを実行するか"
  type        = bool
  default     = true
}

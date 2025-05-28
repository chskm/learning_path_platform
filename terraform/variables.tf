variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-2"
}

variable "app_name" {
  description = "Application name"
  type        = string
  default     = "learning-path-platform"
}

variable "db_username" {
  description = "Aurora database master username"
  type        = string
  sensitive   = true
  default     = "admin"
}

variable "db_password" {
  description = "Aurora database master password"
  type        = string
  sensitive   = true
}
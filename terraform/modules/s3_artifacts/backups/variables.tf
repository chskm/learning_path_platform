# modules/s3_cloudfront/variables.tf
variable "app_name" {
  type = string
}

variable "domain_name" {
  type    = string
  default = ""
}
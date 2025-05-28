# modules/s3_cloudfront/outputs.tf
output "cloudfront_url" {
  value = aws_cloudfront_distribution.frontend.domain_name
}
output "frontend_url" {
  description = "Elastic Beanstalk URL for the frontend"
  value       = module.elastic_beanstalk_frontend.frontend_url
}

output "backend_url" {
  description = "Elastic Beanstalk URL for the backend"
  value       = module.elastic_beanstalk_backend.eb_url
}

output "ml_api_url" {
  description = "API Gateway URL for the ML model"
  value       = module.lambda_api.api_url
}

output "db_endpoint" {
  description = "Aurora database endpoint"
  value       = module.aurora.db_endpoint
}

output "artifacts_bucket" {
  description = "S3 bucket for application artifacts"
  value       = module.s3_artifacts.artifacts_bucket
}

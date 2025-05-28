# modules/lambda_api/outputs.tf
output "api_url" {
  value = "${aws_api_gateway_stage.ml_stage.invoke_url}/recommend"
}

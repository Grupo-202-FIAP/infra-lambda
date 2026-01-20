output "http_api_id" {
  description = "ID do API Gateway HTTP API"
  value       = aws_apigatewayv2_api.crud_api.id 
}

output "stage_name" {
  description = "Nome do stage do API Gateway"
  value       = aws_apigatewayv2_stage.dev.name 
}

output "api_endpoint" {
  description = "URL endpoint do API Gateway"
  value       = aws_apigatewayv2_api.crud_api.api_endpoint
}

output "invoke_url" {
  description = "URL de invocação do API Gateway"
  value       = "${aws_apigatewayv2_api.crud_api.api_endpoint}/${aws_apigatewayv2_stage.dev.name}"
}
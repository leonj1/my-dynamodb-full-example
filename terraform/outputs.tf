output "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  value       = aws_dynamodb_table.example_table.name
}

output "dynamodb_table_arn" {
  description = "ARN of the DynamoDB table"
  value       = aws_dynamodb_table.example_table.arn
}

output "dynamodb_table_hash_key" {
  description = "Hash key of the DynamoDB table"
  value       = aws_dynamodb_table.example_table.hash_key
}

output "dynamodb_endpoint" {
  description = "Endpoint for DynamoDB"
  value       = "http://localstack:4566"
}

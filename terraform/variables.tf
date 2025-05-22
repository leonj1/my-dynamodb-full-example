variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "us-east-1"
}

variable "table_name" {
  description = "Name of the DynamoDB table"
  type        = string
  default     = "example-table"
}

variable "environment" {
  description = "Environment (e.g. local, dev, prod)"
  type        = string
  default     = "local"
}

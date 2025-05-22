# Terraform Configuration for LocalStack DynamoDB

This directory contains Terraform configuration files to create a DynamoDB table in LocalStack.

## Files

- `main.tf` - Main Terraform configuration file with the DynamoDB table definition
- `variables.tf` - Variable definitions
- `outputs.tf` - Output definitions
- `terraform.tfvars` - Default variable values

## Prerequisites

- Terraform installed
- LocalStack running (via docker-compose from the parent directory)

## Usage

1. Initialize Terraform:

```bash
terraform init
```

2. Plan the changes:

```bash
terraform plan
```

3. Apply the changes to create the DynamoDB table:

```bash
terraform apply
```

4. To destroy the resources:

```bash
terraform destroy
```

## Docker Networking

This Terraform configuration is designed to work with Docker's networking capabilities. The configuration uses `localstack` as the hostname (instead of `localhost`) because the Terraform container and the LocalStack container communicate over the Docker network created by docker-compose (`my-dynamodb-full-example_default`).

## Accessing the DynamoDB Table

Once created, you can access the DynamoDB table using the AWS CLI:

### From your host machine:

```bash
aws dynamodb describe-table --table-name example-table --endpoint-url=http://localhost:4566
```

Or list all tables:

```bash
aws dynamodb list-tables --endpoint-url=http://localhost:4566
```

### From inside a Docker container:

If you're accessing the DynamoDB table from another Docker container on the same network, use:

```bash
aws dynamodb describe-table --table-name example-table --endpoint-url=http://localstack:4566
```

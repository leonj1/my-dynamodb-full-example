# LocalStack DynamoDB Example

This project provides a complete local development environment for working with DynamoDB. It includes:

- LocalStack for emulating AWS services locally
- Terraform for infrastructure as code
- Python scripts for DynamoDB CRUD operations
- DynamoDB Dashboard for visual database management

## Prerequisites

- Docker
- Docker Compose
- Make

## Project Structure

- `docker-compose.yml` - Defines LocalStack and DynamoDB Dashboard services
- `Dockerfile.terraform` - Container for running Terraform commands
- `Dockerfile.integration` - Container for running Python integration tests
- `terraform/` - Terraform configuration for DynamoDB tables
- `dynamodb_crud.py` - Python script for CRUD operations

## Using the Makefile

This project uses a Makefile to simplify common operations. Here are the available commands:

### Infrastructure Management

```bash
# Show all available commands
make help

# Start LocalStack container
make localstack-up

# Stop LocalStack container
make localstack-down

# Initialize Terraform
make tf-init

# Plan Terraform changes
make tf-plan

# Apply Terraform configuration to create resources
make tf-up

# Destroy Terraform resources
make tf-down

# Start everything (LocalStack + Terraform resources)
make all-up

# Tear down everything
make all-down
```

### Integration Testing

```bash
# Build the integration test Docker image
make build-integration-image

# Run the integration tests against LocalStack
make integration
```

## Getting Started

1. Start the complete environment:

```bash
make all-up
```

This command will:
- Start the LocalStack container
- Initialize Terraform
- Create the DynamoDB tables defined in the Terraform configuration

2. Access the services:

- LocalStack endpoint: http://localhost:4566
- DynamoDB Dashboard: http://localhost:4567/dynamodb

3. Run the Python CRUD operations:

```bash
# Directly on your machine
pip install -r requirements.txt
python dynamodb_crud.py

# Or using Docker
make integration
```

## Services Enabled

The following AWS services are enabled in this LocalStack setup:
- DynamoDB
- S3
- Lambda
- IAM
- API Gateway
- STS
- CloudFormation

## Default Configuration

- Default region: us-east-1
- Data persistence: Data is persisted in the `/tmp/localstack` directory
- DynamoDB table: `example-table` with hash key `id` and GSIs on `email` and `created_at`

## Stopping the Services

To stop all services and clean up resources:

```bash
make all-down
```

## Docker Networking

This project uses Docker networking to connect the containers:

- Terraform container connects to LocalStack using the Docker network
- Host machine can access LocalStack at `localhost:4566`
- Containers on the same Docker network use `localstack:4566`
- The integration test container runs on the same network to access LocalStack

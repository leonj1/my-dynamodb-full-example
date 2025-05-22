# LocalStack DynamoDB Example

This project contains a Docker Compose setup for running LocalStack, which provides a local AWS cloud stack for development and testing.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Start the LocalStack container:

```bash
docker-compose up -d
```

2. Verify that LocalStack is running:

```bash
docker ps
```

3. Access LocalStack services at:
   - Main endpoint: http://localhost:4566

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

## Stopping the Services

To stop the LocalStack container:

```bash
docker-compose down
```

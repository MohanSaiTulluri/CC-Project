# AWS Deployment Guide for Number Plate Detector

This guide explains how to deploy the Number Plate Detector application to AWS using Docker containers.

## Prerequisites

- AWS Account
- AWS CLI installed and configured
- Docker and Docker Compose installed locally
- OpenAI API key

## Deployment Options

There are several ways to deploy containerized applications on AWS:

1. **Amazon ECS (Elastic Container Service)** - Fully managed container orchestration service
2. **Amazon EKS (Elastic Kubernetes Service)** - Managed Kubernetes service
3. **AWS App Runner** - Fully managed service for containerized applications
4. **Amazon EC2** - Virtual servers in the cloud

This guide will focus on ECS deployment as it provides a good balance of control and ease of use.

## Preparation

1. Build and test your Docker containers locally:

```bash
# Create .env file for the backend
echo "OPENAI_API_KEY=your_actual_openai_api_key" > number-plate-detector-api/.env

# Run both containers
docker-compose up --build
```

2. Create AWS ECR repositories for your images:

```bash
# Create repositories
aws ecr create-repository --repository-name number-plate-detector-frontend
aws ecr create-repository --repository-name number-plate-detector-backend

# Get the ECR registry URL
export ECR_REGISTRY=$(aws ecr describe-repositories --query 'repositories[0].repositoryUri' --output text | cut -d'/' -f1)
```

3. Tag and push your images:

```bash
# Login to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_REGISTRY

# Build, tag and push backend
docker build -t $ECR_REGISTRY/number-plate-detector-backend:latest ./number-plate-detector-api
docker push $ECR_REGISTRY/number-plate-detector-backend:latest

# Build, tag and push frontend
docker build -t $ECR_REGISTRY/number-plate-detector-frontend:latest ./number-plate-detector
docker push $ECR_REGISTRY/number-plate-detector-frontend:latest
```

## AWS ECS Deployment

### 1. Create ECS Cluster

```bash
aws ecs create-cluster --cluster-name number-plate-detector-cluster
```

### 2. Create Task Definitions

Create two task definitions, one for the backend and one for the frontend. Use the AWS console or JSON files:

**Backend Task Definition (backend-task.json):**
```json
{
  "family": "number-plate-detector-backend",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::<your-account-id>:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "<your-account-id>.dkr.ecr.<your-region>.amazonaws.com/number-plate-detector-backend:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8002,
          "hostPort": 8002,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "OPENAI_API_KEY",
          "value": "<your-openai-api-key>"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/number-plate-detector-backend",
          "awslogs-region": "<your-region>",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

**Frontend Task Definition (frontend-task.json):**
```json
{
  "family": "number-plate-detector-frontend",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::<your-account-id>:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "frontend",
      "image": "<your-account-id>.dkr.ecr.<your-region>.amazonaws.com/number-plate-detector-frontend:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 3000,
          "hostPort": 3000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "BACKEND_URL",
          "value": "http://<backend-service-url>:8002"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/number-plate-detector-frontend",
          "awslogs-region": "<your-region>",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

Register the task definitions:
```bash
aws ecs register-task-definition --cli-input-json file://backend-task.json
aws ecs register-task-definition --cli-input-json file://frontend-task.json
```

### 3. Create Security Groups

```bash
# Create backend security group
aws ec2 create-security-group --group-name backend-sg --description "Security group for backend containers" --vpc-id <your-vpc-id>
aws ec2 authorize-security-group-ingress --group-id <backend-sg-id> --protocol tcp --port 8002 --source-group <frontend-sg-id>

# Create frontend security group
aws ec2 create-security-group --group-name frontend-sg --description "Security group for frontend containers" --vpc-id <your-vpc-id>
aws ec2 authorize-security-group-ingress --group-id <frontend-sg-id> --protocol tcp --port 3000 --cidr 0.0.0.0/0
```

### 4. Create ECS Services

**Backend Service:**
```bash
aws ecs create-service \
  --cluster number-plate-detector-cluster \
  --service-name backend-service \
  --task-definition number-plate-detector-backend:1 \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[<subnet-id-1>,<subnet-id-2>],securityGroups=[<backend-sg-id>],assignPublicIp=ENABLED}"
```

**Frontend Service:**
```bash
aws ecs create-service \
  --cluster number-plate-detector-cluster \
  --service-name frontend-service \
  --task-definition number-plate-detector-frontend:1 \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[<subnet-id-1>,<subnet-id-2>],securityGroups=[<frontend-sg-id>],assignPublicIp=ENABLED}"
```

### 5. Create Application Load Balancer (Optional)

For a production setup, you should create an Application Load Balancer for the frontend service and configure HTTPS.

## Alternative: AWS App Runner

For a simpler deployment, consider AWS App Runner:

1. Navigate to AWS App Runner in the AWS Console
2. Click "Create service"
3. Choose "Container registry" as the source
4. Select your ECR repository and image
5. Configure the service settings
6. Set environment variables (e.g., OPENAI_API_KEY for backend)
7. Deploy the service

Deploy the backend first, then deploy the frontend with the backend URL as an environment variable.

## Secure the OpenAI API Key

For production, use AWS Secrets Manager to store your OpenAI API key:

```bash
# Create a secret
aws secretsmanager create-secret \
  --name openai-api-key \
  --secret-string "{\"OPENAI_API_KEY\":\"your-actual-api-key\"}"

# Update your task definition to use the secret
# Replace the environment section with:
"secrets": [
  {
    "name": "OPENAI_API_KEY",
    "valueFrom": "arn:aws:secretsmanager:<region>:<account-id>:secret:openai-api-key:OPENAI_API_KEY::"
  }
]
```

## Monitoring and Scaling

- Set up CloudWatch alarms to monitor CPU and memory usage
- Configure auto-scaling based on load
- Use CloudWatch Logs for application logs

## Cost Optimization

- Use Fargate Spot for non-critical workloads
- Schedule scaling actions for predictable traffic patterns
- Right-size your task definitions based on actual resource usage 
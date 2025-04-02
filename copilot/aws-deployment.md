# AWS Deployment Instructions

This document outlines how to deploy the Cooking Assistant application to AWS using AWS Copilot.

## Prerequisites

- AWS CLI configured with appropriate permissions
- AWS Copilot CLI installed
- Docker installed and running

## Deployment Steps

### 1. Initialize the Application

Run this command from your project root directory:

```bash
copilot init --app cooking-assistant --name cooking-api --type "Load Balanced Web Service" --dockerfile ./Dockerfile --port 8000
```

This initializes a new Copilot application.

### 2. Create an Environment

```bash
copilot env init --name test --profile default --app cooking-assistant
```

This creates a test environment. You can create additional environments like 'prod' if needed.

### 3. Store Your API Key Securely

```bash
aws ssm put-parameter \
  --name /cooking-assistant/anthropic-api-key \
  --value "your-anthropic-api-key-here" \
  --type SecureString
```

Replace `your-anthropic-api-key-here` with your actual Anthropic API key.

### 4. Deploy the Application

```bash
copilot deploy --name cooking-api --env test
```

This builds your Docker image, pushes it to ECR, and deploys the service to your test environment.

### 5. View Service Status

```bash
copilot svc status --name cooking-api --env test
```

This shows the status of your deployed service, including the public endpoint URL.

### 6. View Service Logs

```bash
copilot svc logs --name cooking-api --env test
```

This displays the logs from your running service.

## Cleaning Up

If you want to delete the deployment:

```bash
copilot app delete
```

This will remove all resources created by Copilot, including the ECS service, ALB, ECR repository, and CloudFormation stacks.

## Additional Configuration Options

You can modify the following files to customize your deployment:

- `copilot/cooking-api/manifest.yml`: Service configuration
- `copilot/environments/test/manifest.yml`: Environment configuration

## Troubleshooting

If you encounter issues:

1. Check your service logs: `copilot svc logs`
2. Verify environment variables are correctly set
3. Ensure your API key is properly stored in SSM Parameter Store
4. Check the security groups to ensure traffic can reach your service
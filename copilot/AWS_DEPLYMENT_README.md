# Cooking Assistant AWS Deployment

This document provides an overview of the AWS deployment architecture for the Cooking Assistant application using AWS Copilot.

## Architecture Overview

The Cooking Assistant is deployed as a containerized application with the following AWS services:

- **Amazon ECS (Elastic Container Service)**: Runs the application containers
- **Application Load Balancer**: Distributes incoming traffic across containers
- **Amazon ECR (Elastic Container Registry)**: Stores the Docker container images
- **AWS Secrets Manager**: Securely stores the Anthropic API key
- **Amazon CloudWatch**: Monitors application logs and metrics
- **AWS IAM**: Manages permissions for the services

## Deployment Components

The deployment consists of:

1. **Docker Container**: Packages the application and all dependencies
2. **Service Definition**: Configures how the container runs on ECS
3. **Environment Configuration**: Sets up networking and security
4. **Load Balancer**: Routes HTTP traffic to the service

## Service Configuration

The service is configured with:

- **CPU/Memory**: 256 CPU units, 512MB RAM
- **Autoscaling**: Initially configured for 1 container
- **Health Check**: Monitors the `/health` endpoint
- **Secrets**: Anthropic API key stored securely in SSM Parameter Store

## Scaling Considerations

As your usage grows, consider:

1. **Increasing container resources**: Adjust CPU/memory in the manifest
2. **Enabling autoscaling**: Configure service to scale based on metrics
3. **Adding a database**: For persistent storage of recipes and user preferences

## Monitoring and Maintenance

1. **View logs** with `copilot svc logs`
2. **Check service status** with `copilot svc status` 
3. **Update the service** with `copilot svc deploy` after changes

## Cost Considerations

This deployment uses:
- ECS Fargate (serverless containers)
- Application Load Balancer
- CloudWatch Logs

Estimated monthly cost for low to moderate traffic: $40-80 USD/month

## Security Best Practices

1. API keys are stored in SSM Parameter Store
2. Service has the minimum IAM permissions needed
3. Network traffic is configured for least privilege
4. Security patches are applied through regular container rebuilds

## Next Steps

Consider adding:

1. **Custom domain** with SSL certificate
2. **API authentication** for authorized access
3. **Database integration** for storing user data
4. **Caching layer** to reduce API calls to Anthropic
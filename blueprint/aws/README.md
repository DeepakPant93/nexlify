# Nexlify Terraform Infrastructure Module

This Terraform module provisions AWS infrastructure for the [Nexlify](https://github.com/DeepakPant93/nexlify) project - a Retrieval-Augmented Generation (RAG) AI chatbot integrated with GitHub Copilot.

## Architecture Overview

The module creates the following infrastructure:

- **VPC** with public and private subnets across multiple availability zones
- **NAT Gateway** in public subnet for private subnet internet access
- **Internet Gateway** for public subnet internet access
- **EC2 Instance** in public subnet for application services (FastAPI, AI Agentics)
- **EC2 Instance** in private subnet for Qdrant vector database
- **Security Groups** with proper port configurations:
  - Web App SG: Ports 7860, 8000, 80, 443, 22
  - Database SG: Ports 6333, 6334, 22

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **Terraform** >= 1.0 installed
3. **AWS CLI** configured with credentials
4. **AWS Key Pair** created in your target region

## Quick Start

1. **Clone and navigate to the module directory:**
   ```bash
   git clone <this-repository>
   cd blueprint
   ```

2. **Copy and customize variables:**
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your specific values
   ```

3. **Initialize and apply:**
   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

4. **Access your infrastructure:**
   ```bash
   # SSH to public instance
   ssh -i ~/.ssh/your-key.pem ec2-user@<public-ip>
   
   # SSH to private instance (via bastion)
   ssh -i ~/.ssh/your-key.pem -J ec2-user@<public-ip> ec2-user@<private-ip>
   ```

## Configuration

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `key_name` | AWS Key Pair name | `"my-key-pair"` |

### Important Variables

| Variable | Description | Default | Notes |
|----------|-------------|---------|-------|
| `aws_region` | AWS region | `"ap-south-1"` | Choose based on your location |
| `project_name` | Project name for resource naming | `"nexlify"` | Used in all resource names |
| `environment` | Environment (dev/staging/prod) | `"dev"` | Affects resource naming |
| `vpc_cidr` | VPC CIDR block | `"10.0.0.0/16"` | Adjust based on your network needs |
| `public_instance_type` | Public EC2 instance type | `"t3.medium"` | For FastAPI services |
| `private_instance_type` | Private EC2 instance type | `"t3.medium"` | For Qdrant database |
| `single_nat_gateway` | Use single NAT Gateway | `true` | Set false for HA (increases cost) |
| `ssh_cidr_blocks` | CIDR blocks for SSH access | `["0.0.0.0/0"]` | Restrict for security |

## Application Ports

| Port | Service | Location | Description |
|------|---------|----------|-------------|
| 7860 | Data Ingestion | Public Instance | FastAPI data ingestion service |
| 8001 | AI Agentics | Public Instance | AI Agentics service |
| 6333 | Qdrant REST | Private Instance | Qdrant vector database REST API |
| 6334 | Qdrant gRPC | Private Instance | Qdrant vector database gRPC API |

## Infrastructure Deployment

### Terraform Cloud

To **create or update** the infrastructure for the Nexlify app, follow these steps:

1. Go to the [Terraform Cloud Nexlify Workspace](https://app.terraform.io/app/dpant_academy/workspaces/nexlify-dev).
2. Ensure you are in the correct workspace: `nexlify-dev`.
3. Click on **"+ New Run"**.
4. This will trigger the Terraform **plan and apply** pipeline.
5. Terraform will automatically create or update the infrastructure as defined in the configuration.

> 💡 Make sure all necessary variables and credentials are correctly set in the workspace before starting a new run.


## Post-Deployment Setup

### 1. Deploy Nexlify Application

SSH to the public instance and clone the repository:

```bash
ssh -i ~/.ssh/your-key.pem ec2-user@<public-ip>
cd /opt/nexlify
git clone https://github.com/DeepakPant93/nexlify.git .
```

### 2. Configure Services

The instances come pre-configured with:
- **Public Instance**: Docker, Python 3.11, systemd services for Nexlify
- **Private Instance**: Docker, Qdrant running in container, automated backups

### 3. Start Services

```bash
# On public instance
sudo systemctl start nexlify-data-ingestion
sudo systemctl start nexlify-ai-agentics

# Check Qdrant status on private instance
sudo systemctl status qdrant-nexlify
```

## Security Considerations

### Network Security
- Private subnet has no direct internet access (uses NAT Gateway)
- Security groups restrict access to necessary ports only
- Database is isolated in private subnet

### Access Control
- SSH access controlled via `ssh_cidr_blocks` variable
- Database only accessible from application security group
- Consider using AWS Systems Manager Session Manager for secure access

### Recommendations for Production
- Use restrictive CIDR blocks for SSH access
- Enable VPC Flow Logs
- Use AWS Secrets Manager for sensitive configuration
- Implement proper backup strategies
- Use multiple NAT Gateways for high availability

## Cost Optimization

### Default Settings (Cost-Optimized)
- Single NAT Gateway (`single_nat_gateway = true`)
- t3.medium instances (adjust based on workload)
- GP3 storage volumes

### For Production (Higher Availability)
```hcl
single_nat_gateway = false  # Multiple NAT Gateways
public_instance_type = "t3.large"
private_instance_type = "r5.large"  # Better for database workloads
```

## Troubleshooting

### Common Issues

1. **SSH Connection Refused**
   - Check security group allows your IP
   - Verify key pair name is correct
   - Ensure instance is running

2. **Services Not Starting**
   - Check user-data execution: `sudo cat /var/log/user-data.log`
   - Verify Docker is running: `sudo systemctl status docker`
   - Check service logs: `sudo journalctl -u service-name`

3. **Qdrant Not Accessible**
   - Verify container is running: `docker ps`
   - Check logs: `docker logs qdrant-nexlify`
   - Test connectivity: `curl http://localhost:6333/health`

### Useful Commands

```bash
# Check instance metadata
curl http://169.254.169.254/latest/meta-data/

# View all systemd services
systemctl list-units --type=service

# Monitor resource usage
htop

# Check Docker containers
docker ps -a
```

## Outputs

The module provides comprehensive outputs including:

- VPC and subnet IDs
- Instance IPs and connection strings
- Security group IDs
- Application URLs
- Resource ARNs

---

**Note**: This module is designed for the Nexlify RAG AI chatbot project. Customize variables and configurations based on your specific requirements and security policies.
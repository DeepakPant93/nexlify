# variables.tf - Input variables for Nexlify Terraform module

# Project Configuration
variable "project_name" {
  description = "Name of the project used for resource naming and tagging"
  type        = string
  default     = "nexlify"

  validation {
    condition     = length(var.project_name) > 0 && length(var.project_name) <= 20
    error_message = "Project name must be between 1 and 20 characters."
  }
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}

# AWS Configuration
variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "ap-south-1"
}

# VPC Configuration
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"

  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "VPC CIDR must be a valid IPv4 CIDR block."
  }
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]

  validation {
    condition     = length(var.public_subnet_cidrs) >= 1
    error_message = "At least one public subnet CIDR must be provided."
  }
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.20.0/24"]

  validation {
    condition     = length(var.private_subnet_cidrs) >= 1
    error_message = "At least one private subnet CIDR must be provided."
  }
}

variable "single_nat_gateway" {
  description = "Use single NAT Gateway for all private subnets (cost optimization)"
  type        = bool
  default     = true
}

# EC2 Configuration
variable "ec2_ami" {
  description = "AMI ID for EC2 instances (leave empty to use latest Amazon Linux 2023)"
  type        = string
  default     = "ami-0d0ad8bb301edb745"
}

variable "public_instance_type" {
  description = "Instance type for public subnet EC2 instance"
  type        = string
  default     = "t3.medium"

  validation {
    condition = contains([
      "t3.micro", "t3.small", "t3.medium", "t3.large", "t3.xlarge",
      "t3a.micro", "t3a.small", "t3a.medium", "t3a.large", "t3a.xlarge",
      "m5.large", "m5.xlarge", "m5.2xlarge",
      "c5.large", "c5.xlarge", "c5.2xlarge"
    ], var.public_instance_type)
    error_message = "Instance type must be a valid AWS instance type."
  }
}

variable "private_instance_type" {
  description = "Instance type for private subnet EC2 instance (database server)"
  type        = string
  default     = "t3.medium"

  validation {
    condition = contains([
      "t3.micro", "t3.small", "t3.medium", "t3.large", "t3.xlarge", "t3.2xlarge",
      "t3a.micro", "t3a.small", "t3a.medium", "t3a.large", "t3a.xlarge", "t3a.2xlarge",
      "m5.large", "m5.xlarge", "m5.2xlarge", "m5.4xlarge",
      "r5.large", "r5.xlarge", "r5.2xlarge", "r5.4xlarge"
    ], var.private_instance_type)
    error_message = "Instance type must be a valid AWS instance type."
  }
}

variable "key_name" {
  description = "AWS Key Pair name for EC2 instances"
  type        = string

  validation {
    condition     = length(var.key_name) > 0
    error_message = "Key name must be provided."
  }
}

variable "root_volume_size" {
  description = "Size of the root EBS volume in GB"
  type        = number
  default     = 20

  validation {
    condition     = var.root_volume_size >= 8 && var.root_volume_size <= 1000
    error_message = "Root volume size must be between 8 and 1000 GB."
  }
}

# Security Configuration
variable "ssh_cidr_blocks" {
  description = "CIDR blocks allowed for SSH access"
  type        = list(string)
  default     = ["0.0.0.0/0"]

  validation {
    condition     = length(var.ssh_cidr_blocks) > 0
    error_message = "At least one SSH CIDR block must be provided."
  }
}

# Tagging
variable "common_tags" {
  description = "Common tags to be applied to all resources"
  type        = map(string)
  default = {
    Project     = "Nexlify"
    ManagedBy   = "Terraform"
    Owner       = "DevOps"
    Application = "RAG-AI-Chatbot"
  }
}

# Port Configuration (for documentation and future use)
variable "nexlify_ports" {
  description = "Ports used by Nexlify application components"
  type = object({
    data_ingestion_service_port = number # Streamlit/Gradio applications
    agentic_ai_service_port     = number # FastAPI data ingestion service
    qdrant_rest_port            = number # AI Agentics service
    qdrant_grpc_port            = number # Qdrant gRPC API
  })
  default = {
    data_ingestion_service_port = 7860
    agentic_ai_service_port     = 8000
    qdrant_rest_port            = 6333
    qdrant_grpc_port            = 6334
  }
}
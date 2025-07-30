# main.tf - Root module for Nexlify Terraform Infrastructure
# This file orchestrates the creation of VPC, Security Groups, and EC2 instances

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = var.aws_region
}

# Get availability zones
data "aws_availability_zones" "available" {
  state = "available"

  filter {
    name   = "opt-in-status"
    values = ["opt-in-not-required"]
  }
}

locals {
  # Use only first 2 AZs to avoid constrained zones
  selected_azs = slice(data.aws_availability_zones.available.names, 0, 2)
}

# VPC Module
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${var.project_name}-vpc"
  cidr = var.vpc_cidr

  # azs             = data.aws_availability_zones.available.names
  azs             = local.selected_azs
  public_subnets  = var.public_subnet_cidrs
  private_subnets = var.private_subnet_cidrs

  enable_ipv6 = false

  enable_nat_gateway = true
  enable_vpn_gateway = false
  single_nat_gateway = var.single_nat_gateway

  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(var.common_tags, {
    Name        = "${var.project_name}-vpc"
    Terraform   = "true"
    Environment = var.environment
  })

  public_subnet_tags = merge(var.common_tags, {
    Name = "${var.project_name}-public-subnet"
    Type = "public"
  })

  private_subnet_tags = merge(var.common_tags, {
    Name = "${var.project_name}-private-subnet"
    Type = "private"
  })

  nat_gateway_tags = merge(var.common_tags, {
    Name = "${var.project_name}-nat-gateway"
  })

  igw_tags = merge(var.common_tags, {
    Name = "${var.project_name}-igw"
  })
}

# Security Group for FastAPI and Web Apps (ports 7860, 8000)
resource "aws_security_group" "web_app_sg" {
  name        = "${var.project_name}-web-app-sg"
  description = "Security group for FastAPI and web applications"
  vpc_id      = module.vpc.vpc_id

  # HTTP port 7860 (for web applications like Streamlit)
  ingress {
    description = "Data Ingestion service port 7860"
    from_port   = var.nexlify_ports["data_ingestion_service_port"]
    to_port     = var.nexlify_ports["data_ingestion_service_port"]
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTP port 8000 (for FastAPI applications)
  ingress {
    description = "Agentic AI application port 8000"
    from_port   = var.nexlify_ports["agentic_ai_service_port"]
    to_port     = var.nexlify_ports["agentic_ai_service_port"]
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # SSH access
  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.ssh_cidr_blocks
  }

  # HTTPS
  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTP
  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound rules
  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = merge(var.common_tags, {
    Name    = "${var.project_name}-web-app-sg"
    Purpose = "Web application security group"
  })
}

# Security Group for Qdrant Database (port 6333)
resource "aws_security_group" "database_sg" {
  name        = "${var.project_name}-database-sg"
  description = "Security group for Qdrant database"
  vpc_id      = module.vpc.vpc_id

  # Qdrant REST API port 6333
  ingress {
    description     = "Qdrant REST API port 6333"
    from_port       = var.nexlify_ports["qdrant_rest_port"]
    to_port         = var.nexlify_ports["qdrant_rest_port"]
    protocol        = "tcp"
    security_groups = [aws_security_group.web_app_sg.id]
  }

  # Qdrant gRPC port 6334 (for internal communication)
  ingress {
    description     = "Qdrant gRPC port 6334"
    from_port       = var.nexlify_ports["qdrant_grpc_port"]
    to_port         = var.nexlify_ports["qdrant_grpc_port"]
    protocol        = "tcp"
    security_groups = [aws_security_group.web_app_sg.id]
  }

  # SSH access from bastion or management network
  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.ssh_cidr_blocks
  }

  # Outbound rules
  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = merge(var.common_tags, {
    Name    = "${var.project_name}-database-sg"
    Purpose = "Database security group"
  })
}

# Get latest Amazon Linux 2023 AMI
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# EC2 Instance in Public Subnet (for app installation)
resource "aws_instance" "public_instance" {
  ami                         = var.ec2_ami != "" ? var.ec2_ami : data.aws_ami.amazon_linux.id
  instance_type               = var.public_instance_type
  key_name                    = var.key_name
  subnet_id                   = module.vpc.public_subnets[0]
  vpc_security_group_ids      = [aws_security_group.web_app_sg.id]
  associate_public_ip_address = true

  root_block_device {
    volume_type = "gp3"
    volume_size = var.root_volume_size
    encrypted   = true
  }

  user_data = base64encode(templatefile("${path.module}/user-data/public-instance.sh", {
    project_name = var.project_name
  }))

  tags = merge(var.common_tags, {
    Name        = "${var.project_name}-public-instance"
    Environment = var.environment
    Purpose     = "Application server"
    Tier        = "public"
  })
}

# EC2 Instance in Private Subnet (for database)
resource "aws_instance" "private_instance" {
  ami                    = var.ec2_ami != "" ? var.ec2_ami : data.aws_ami.amazon_linux.id
  instance_type          = var.private_instance_type
  key_name               = var.key_name
  subnet_id              = module.vpc.private_subnets[0]
  vpc_security_group_ids = [aws_security_group.database_sg.id]

  root_block_device {
    volume_type = "gp3"
    volume_size = var.root_volume_size
    encrypted   = true
  }

  user_data = base64encode(templatefile("${path.module}/user-data/private-instance.sh", {
    project_name = var.project_name
  }))

  tags = merge(var.common_tags, {
    Name        = "${var.project_name}-private-instance"
    Environment = var.environment
    Purpose     = "Database server"
    Tier        = "private"
  })
}
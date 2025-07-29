# outputs.tf - Output values for Nexlify Terraform module

# VPC Outputs
output "vpc_id" {
  description = "ID of the VPC"
  value       = module.vpc.vpc_id
}

output "vpc_cidr_block" {
  description = "The CIDR block of the VPC"
  value       = module.vpc.vpc_cidr_block
}

output "vpc_arn" {
  description = "The ARN of the VPC"
  value       = module.vpc.vpc_arn
}

# Subnet Outputs
output "public_subnet_ids" {
  description = "List of IDs of public subnets"
  value       = module.vpc.public_subnets
}

output "private_subnet_ids" {
  description = "List of IDs of private subnets"
  value       = module.vpc.private_subnets
}

output "public_subnet_cidrs" {
  description = "List of CIDR blocks of public subnets"
  value       = module.vpc.public_subnets_cidr_blocks
}

output "private_subnet_cidrs" {
  description = "List of CIDR blocks of private subnets"
  value       = module.vpc.private_subnets_cidr_blocks
}

# Internet Gateway Output
output "internet_gateway_id" {
  description = "The ID of the Internet Gateway"
  value       = module.vpc.igw_id
}

# NAT Gateway Outputs
output "nat_gateway_ids" {
  description = "List of IDs of the NAT Gateways"
  value       = module.vpc.natgw_ids
}

output "nat_public_ips" {
  description = "List of public Elastic IPs created for AWS NAT Gateway"
  value       = module.vpc.nat_public_ips
}

# Security Group Outputs
output "web_app_security_group_id" {
  description = "ID of the web application security group"
  value       = aws_security_group.web_app_sg.id
}

output "web_app_security_group_arn" {
  description = "ARN of the web application security group"
  value       = aws_security_group.web_app_sg.arn
}

output "database_security_group_id" {
  description = "ID of the database security group"
  value       = aws_security_group.database_sg.id
}

output "database_security_group_arn" {
  description = "ARN of the database security group"
  value       = aws_security_group.database_sg.arn
}

# EC2 Instance Outputs
output "public_instance_id" {
  description = "ID of the public EC2 instance"
  value       = aws_instance.public_instance.id
}

output "public_instance_public_ip" {
  description = "Public IP address of the public EC2 instance"
  value       = aws_instance.public_instance.public_ip
}

output "public_instance_private_ip" {
  description = "Private IP address of the public EC2 instance"
  value       = aws_instance.public_instance.private_ip
}

output "public_instance_public_dns" {
  description = "Public DNS name of the public EC2 instance"
  value       = aws_instance.public_instance.public_dns
}

output "private_instance_id" {
  description = "ID of the private EC2 instance"
  value       = aws_instance.private_instance.id
}

output "private_instance_private_ip" {
  description = "Private IP address of the private EC2 instance"
  value       = aws_instance.private_instance.private_ip
}

output "private_instance_private_dns" {
  description = "Private DNS name of the private EC2 instance"
  value       = aws_instance.private_instance.private_dns
}

# Application URLs
output "nexlify_application_urls" {
  description = "URLs for accessing Nexlify applications"
  value = {
    data_ingestion_service = "http://${aws_instance.public_instance.public_ip}:8000"
    ai_agentics_service    = "http://${aws_instance.public_instance.public_ip}:8001"
    web_interface          = "http://${aws_instance.public_instance.public_ip}:7860"
    qdrant_dashboard       = "http://${aws_instance.private_instance.private_ip}:6333/dashboard"
  }
}

# Connection Information
output "connection_info" {
  description = "Information for connecting to the instances"
  value = {
    public_instance_ssh  = "ssh -i ~/.ssh/${var.key_name}.pem ec2-user@${aws_instance.public_instance.public_ip}"
    private_instance_ssh = "ssh -i ~/.ssh/${var.key_name}.pem -J ec2-user@${aws_instance.public_instance.public_ip} ec2-user@${aws_instance.private_instance.private_ip}"
  }
  sensitive = false
}

# Resource ARNs for advanced configurations
output "resource_arns" {
  description = "ARNs of created resources"
  value = {
    vpc                     = module.vpc.vpc_arn
    public_instance         = aws_instance.public_instance.arn
    private_instance        = aws_instance.private_instance.arn
    web_app_security_group  = aws_security_group.web_app_sg.arn
    database_security_group = aws_security_group.database_sg.arn
  }
}

# Cost Optimization Information
output "cost_optimization_info" {
  description = "Information about cost optimization settings"
  value = {
    single_nat_gateway    = var.single_nat_gateway
    nat_gateway_count     = var.single_nat_gateway ? 1 : length(var.private_subnet_cidrs)
    public_instance_type  = var.public_instance_type
    private_instance_type = var.private_instance_type
  }
}
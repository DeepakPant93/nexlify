# Nexlify Blueprint: Multi-Cloud Infrastructure Provisioning

This `blueprint` folder contains the infrastructure-as-code (IaC) templates to provision the core cloud resources for the Nexlify stack. It supports both **AWS** and **Azure** cloud providers, each with its own complete and production-ready Terraform configuration.

## Structure

```
blueprint/
├── aws/
│   ├── ... # Terraform scripts for AWS
│   └── README.md
└── azure/
    ├── ... # Terraform scripts for Azure
    └── README.md
```

## Overview

### AWS Infrastructure
- Terraform provisioning for the Nexlify stack on Amazon Web Services.
- Details include VPC, subnets, EC2 instances, security groups, and all core network/app resources.
- For deployment instructions, variables, output references, and customization, see [blueprint/aws/README.md](./aws/README.md).

### Azure Infrastructure
- Terraform code to create the baseline Azure cloud infrastructure for Nexlify.
- Includes resource group setup, virtual networks, subnets, NAT gateway, NSGs, and secure VM instances.
- Uses Terraform Cloud for remote state and safe collaboration.
- Full details, variable setup, credential generation commands, and usage guidance can be found in [blueprint/azure/README.md](./azure/README.md).

## How to Use

1. **Choose your cloud provider:**
   - For AWS, navigate to `blueprint/aws/`
   - For Azure, navigate to `blueprint/azure/`

2. **Read the respective `README.md`:**
   - Each subfolder’s README covers prerequisites, how to get cloud credentials, deployment steps (init, plan, apply), Terraform variable requirements, outputs, and best practices.

3. **Run Terraform as directed:**
   - Adopt the steps in the respective folder’s README to deploy or destroy infrastructure.

## Notes

- Both subfolders are self-contained; you do **not** need to mix files between AWS and Azure.
- Designed for clarity, safety, and extendability for both public cloud environments.

## License

MIT License — see the root [LICENSE](../LICENSE).

For any issues or support, please open an issue in the [Nexlify GitHub repository](https://github.com/DeepakPant93/nexlify).

**Deploy Nexlify the way that fits your cloud strategy—start in AWS or Azure, and scale with confidence!**
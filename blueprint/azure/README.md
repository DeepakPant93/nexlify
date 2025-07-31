# Nexlify Azure Infrastructure

This directory contains Terraform code for provisioning the Azure cloud foundation of the Nexlify stack, with state managed securely in Terraform Cloud.

## Features

| Component            | Details                                                                                                  |
|----------------------|----------------------------------------------------------------------------------------------------------|
| **Resource Group**   | Central India (`centralindia`)                                                                           |
| **VNet**             | 10.0.0.0/16, with public (10.0.1.0/24) and private (10.0.2.0/24) subnets                                |
| **NAT Gateway**      | Standard SKU, Zone 1, static public IP, associated to private subnet for outbound egress                 |
| **NSGs**             | `nsg-app`: TCP 7860, 8000, 22  `nsg-db`: TCP 6333, 22                                                |
| **Virtual Machines** | Ubuntu 22.04 LTS Gen2, Trusted Launch, 30GB Premium SSD, one per subnet                                  |
| **Variables**        | Region, zone, tags, VM size, admin credentials, and required Azure service principal credentials          |
| **Backend**          | Remote state and locking via Terraform Cloud                                                             |
| **Outputs**          | Public IP (App VM), Private IP (DB VM), VNet resource ID                                                 |

## Requirements

- **Terraform ≥ 1.6**
- **Provider:** `azurerm` (~> 4.37.0)
- **Terraform Cloud** workspace, API token, and organization
- **Azure subscription** in Central India, sufficient permissions

## How to Obtain Required Azure Credentials

You must provide credentials for deploying resources. Use the Azure CLI as follows:

### 1. Log in to Azure

```sh
az login
```
_This will open a browser window for you to log in._

### 2. Get Your Subscription ID

```sh
az account show
```
_Look at the `id` field in the output. This is your `subscription_id` (e.g., `31356ee6-8cc8-4397-b16d-a7a2c3eec210`)._

### 3. Create a Service Principal for Terraform

```sh
az ad sp create-for-rbac --name "nexlify-sp" --role Contributor --scopes /subscriptions/31356ee6-8cc8-4397-b16d-a7a2c3eec210 --sdk-auth
```
_This command will output JSON with the required variables:_

```json
{
  "clientId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "clientSecret": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "subscriptionId": "31356ee6-8cc8-4397-b16d-a7a2c3eec210",
  "tenantId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  ...
}
```

**Map these as:**

- `subscription_id`  →  `subscriptionId`
- `client_id`        →  `clientId`
- `client_secret`    →  `clientSecret`
- `tenant_id`        →  `tenantId`

**_Keep your `clientSecret` safe!_**


## GitHub Repository Secrets for CI/CD Setup

Add these secrets in your GitHub repo settings under Secrets and variables > Actions. They're needed for Azure, VMs, Docker, GitHub, Gemini, and Terraform integrations.

- **APP_VM_PASSWORD**: Password for both VMs.
- **APP_VM_USER**: VM username (default: `azureuser`).
- **ARM_CLIENT_ID**: Azure Service Principal Client ID (generated using `az ad sp create-for-rbac ...` command, copy `clientId`).
- **ARM_CLIENT_SECRET**: Azure Service Principal secret (generated using `az ad sp create-for-rbac ...` command output).
- **DOCKER_PASSWORD**: Docker Hub Personal Access Token (generate from https://app.docker.com/accounts/<username>/settings/personal-access-tokens).
- **DOCKER_USERNAME**: Your Docker Hub username.
- **GH_PAT**: GitHub PAT with `repo` scope (used to set VM IP secrets, such as PRIVATE_VM_PRIVATE_IP and PUBLIC_VM_PUBLIC_IP).
- **MODEL_API_KEY**: Gemini API key (create one at https://aistudio.google.com/app/apikey).
- **TF_API_TOKEN**: Terraform Cloud API token (generate one at https://app.terraform.io/app/settings/tokens).


## Deploying with Terraform Cloud

This repo is set up to use Terraform Cloud for state management. In `main.tf`, the backend is configured like so:

```hcl
terraform {
  required_version = ">= 1.6"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.37.0"
    }
  }
  cloud {
    organization = "dpant_academy"
    workspaces {
      name = "nexlify-azure-dev"
    }
  }
}
```

**Azure authentication is provided via the following variables:**
- `subscription_id`
- `client_id`
- `client_secret`
- `tenant_id`

**You must set these via:**
- The [Terraform Cloud workspace UI](https://app.terraform.io) (recommended, mark `client_secret` as sensitive), or  
- Command-line flags (e.g., `-var="client_secret=YOUR_CLIENT_SECRET"`) during plan/apply.

## Deploy Steps

1. **Initialize and Plan**
   ```sh
   terraform init
   terraform plan \
     -var="subscription_id=..." \
     -var="client_id=..." \
     -var="client_secret=..." \
     -var="tenant_id=..."
   ```

2. **Apply**
   ```sh
   terraform apply \
     -var="subscription_id=..." \
     -var="client_id=..." \
     -var="client_secret=..." \
     -var="tenant_id=..."
   ```

3. **Outputs**
   ```
   terraform output public_vm_ip
   terraform output private_vm_private_ip
   terraform output vnet_id
   ```

## Outputs

- **public_vm_ip**: Public IP of the application (public) VM
- **private_vm_private_ip**: Private IP of the database (private) VM
- **vnet_id**: The resource ID of the created Virtual Network

## Best Practices

- Store sensitive values (`client_secret`, VM admin password) in Terraform Cloud as **sensitive** variables.
- Restrict SSH/port 22 access to trusted IPs for production.
- Keep your state in Terraform Cloud for safety and collaboration.
- Audit Terraform Cloud workspace activity regularly.

## Support

For help, open an issue at: [https://github.com/DeepakPant93/nexlify](https://github.com/DeepakPant93/nexlify)

## License

MIT License — see [LICENSE](https://github.com/DeepakPant93/nexlify/blob/main/LICENSE).

**Deploy confidently. Nexlify Azure infrastructure is ready for production workloads with Terraform Cloud.**
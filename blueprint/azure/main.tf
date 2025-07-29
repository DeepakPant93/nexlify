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

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

resource "azurerm_resource_group" "this" {
  name     = "${var.resource_group_name}-${terraform.workspace}"
  location = var.region
  tags     = var.tags
}

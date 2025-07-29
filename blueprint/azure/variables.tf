variable "subscription_id" {
  description = "Azure subscription ID"
  type        = string
  default     = "31356ee6-8cc8-4397-b16d-a7a2c3eec210"

}

variable "client_id" {
  description = "Azure client ID"
  type        = string

}

variable "client_secret" {
  description = "Azure client secret"
  type        = string

}

variable "tenant_id" {
  description = "Azure tenant ID"
  type        = string
  default     = "2e714ce2-9880-4896-a5ff-7754ff57fd86"

}


variable "name_prefix" {
  description = "Prefix for all resources"
  type        = string
  default     = "nexlify"
}

variable "region" {
  description = "Azure region"
  type        = string
  default     = "centralindia"
}

variable "zone" {
  description = "Availability Zone number"
  type        = number
  default     = 1
}

variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
  default     = "nexlify-rg"
}

variable "vm_size" {
  description = "Azure VM size"
  type        = string
  default     = "Standard_B2s"
}

variable "admin_username" {
  description = "Admin user for VMs"
  type        = string
  default     = "azureuser"
}

variable "admin_password" {
  description = "Admin password for VMs (sensitive—do not commit to version control)"
  type        = string
  sensitive   = true

  validation {
    condition = (
      length(var.admin_password) >= 12 &&
      (
        (length(regexall("[a-z]", var.admin_password)) > 0 ? 1 : 0) +
        (length(regexall("[A-Z]", var.admin_password)) > 0 ? 1 : 0) +
        (length(regexall("[0-9]", var.admin_password)) > 0 ? 1 : 0) +
        (length(regexall("[!@#$%^&*()_+-=\\[\\]{}|;':\",.<>?/]", var.admin_password)) > 0 ? 1 : 0)
      ) >= 3
    )
    error_message = "Password must be at least 12 characters long and include at least 3 of the following: lowercase letters (a-z), uppercase letters (A-Z), numbers (0-9), or special characters (e.g., !@#$%^&*()_+-=[]{}|;':\",.<>?/)."
  }
}


variable "tags" {
  description = "Map of tags"
  type        = map(string)
  default     = {}
}

variable "app_ports" {
  description = "List of ports for app NSG"
  type        = list(number)
  default     = [7860, 8000]
}

variable "compose_file_path" {
  description = "Path on VM to place docker-compose.yml"
  type        = string
  default     = "/home/azureuser/docker-compose.yml" # Adjust to match admin_username
}

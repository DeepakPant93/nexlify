# Nexlify Terraform Infrastructure Module (Azure SPecific)

This module provisions the baseline Azure infrastructure for the Nexlify stack.

## Features
| Component | Details |
|-----------|---------|
| Resource Group | Central India (`centralindia`) |
| VNet | 10.0.0.0/16 with **public** (10.0.1.0/24) and **private** (10.0.2.0/24) subnets |
| NAT Gateway | Standard SKU, zonal (Zone 1), static public IP, associated to private subnet for outbound egress |
| NSGs | `nsg-app` (TCP 7860, 8000 inbound) and `nsg-db` (TCP 6333 inbound) |
| Virtual Machines | Ubuntu 22.04 LTS Gen2, Trusted Launch (secure boot + vTPM), 30 GB Premium SSD, one per subnet |
| Variables | Region, zone, tags, VM size, SSH key, names |
| Outputs | Public IP of app VM, private IP of DB VM, VNet ID |

> **Trusted Launch** is enabled via `security_type = "TrustedLaunch"` and `uefi_settings { secure_boot_enabled = true vtpm_enabled = true }` ([Azure doc 16][16]).

## Quick start

output "public_vm_ip" {
  value       = azurerm_public_ip.public_vm.ip_address
  description = "Public IP of the application VM"
}

output "private_vm_private_ip" {
  value       = azurerm_network_interface.private.private_ip_address
  description = "Private IP of the database VM"
}

output "vnet_id" {
  value = azurerm_virtual_network.this.id
}

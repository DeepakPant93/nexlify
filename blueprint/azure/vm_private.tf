resource "azurerm_network_interface" "private" {
  name                = "${var.name_prefix}-nic-private"
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
  ip_configuration {
    name                          = "ipconfig"
    subnet_id                     = azurerm_subnet.private.id
    private_ip_address_allocation = "Dynamic"
  }
  tags = var.tags
}

resource "azurerm_network_interface_security_group_association" "assoc_private" {
  network_interface_id      = azurerm_network_interface.private.id
  network_security_group_id = azurerm_network_security_group.db.id
}

resource "azurerm_linux_virtual_machine" "private" {
  name                            = "${var.name_prefix}-vm-private"
  location                        = azurerm_resource_group.this.location
  resource_group_name             = azurerm_resource_group.this.name
  size                            = var.vm_size
  admin_username                  = var.admin_username
  admin_password                  = var.admin_password
  disable_password_authentication = false
  network_interface_ids           = [azurerm_network_interface.private.id]


  os_disk {
    name                 = "${var.name_prefix}-osdisk-private"
    caching              = "ReadWrite"
    storage_account_type = "Premium_LRS"
    disk_size_gb         = 30
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }

  user_data = base64encode(file("user-data/db.sh"))

  tags = var.tags
}

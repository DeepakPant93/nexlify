#!/bin/bash
# user-data for public instance (Application Server)

# Update system
yum update -y

# Install Docker
yum install -y docker
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Install Python 3.11 and pip
yum install -y python3.11 python3.11-pip git

# Create application directory
mkdir -p /opt/${project_name}
chown ec2-user:ec2-user /opt/${project_name}

# Install development tools
yum groupinstall -y "Development Tools"
yum install -y python3.11-devel

# Create systemd service for Nexlify applications
cat > /etc/systemd/system/nexlify-data-ingestion.service << EOF
[Unit]
Description=Nexlify Data Ingestion Service
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/opt/${project_name}/data-ingestion-server
ExecStart=/usr/bin/python3.11 -m uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

cat > /etc/systemd/system/nexlify-ai-agentics.service << EOF
[Unit]
Description=Nexlify AI Agentics Service
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/opt/${project_name}/nexlify-ai-agentics-server
ExecStart=/usr/bin/python3.11 -m uvicorn main:app --host 0.0.0.0 --port 8001
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable services (they will be started manually after code deployment)
systemctl daemon-reload

echo "Public instance initialization completed" > /var/log/user-data.log
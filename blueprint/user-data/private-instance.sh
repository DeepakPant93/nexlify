#!/bin/bash
# user-data for private instance (Database Server)

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

# Create directories
mkdir -p /opt/${project_name}/qdrant
mkdir -p /opt/${project_name}/data
chown -R ec2-user:ec2-user /opt/${project_name}

# Create Docker Compose file for Qdrant
cat > /opt/${project_name}/docker-compose.yml << EOF
version: '3.8'

services:
  qdrant:
    image: qdrant/qdrant:latest
    container_name: qdrant-${project_name}
    restart: always
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - ./data:/qdrant/storage:z
    environment:
      - QDRANT__SERVICE__HTTP_PORT=6333
      - QDRANT__SERVICE__GRPC_PORT=6334
    command:
      - ./qdrant
      - --config-path
      - config/production.yaml
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - qdrant-network

networks:
  qdrant-network:
    driver: bridge
EOF

chown ec2-user:ec2-user /opt/${project_name}/docker-compose.yml

# Create Qdrant systemd service
cat > /etc/systemd/system/qdrant-${project_name}.service << EOF
[Unit]
Description=Qdrant Vector Database for ${project_name}
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
User=ec2-user
Group=ec2-user
WorkingDirectory=/opt/${project_name}
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

# Enable and start Qdrant service
systemctl daemon-reload
systemctl enable qdrant-${project_name}.service
systemctl start qdrant-${project_name}.service

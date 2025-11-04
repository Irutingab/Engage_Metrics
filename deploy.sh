#!/bin/bash

# Deployment script for DigitalOcean/VPS

set -e

echo "🚀 Deploying EngageMetrics..."

# Update system
echo "📦 Updating system packages..."
apt-get update && apt-get upgrade -y

# Install Docker if not present
if ! command -v docker &> /dev/null; then
    echo "🐳 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
fi

# Install Docker Compose if not present
if ! command -v docker-compose &> /dev/null; then
    echo "🐳 Installing Docker Compose..."
    apt-get install docker-compose -y
fi

# Clone or update repository
if [ -d "Engage_Metrics" ]; then
    echo "📥 Updating repository..."
    cd Engage_Metrics
    git pull
else
    echo "📥 Cloning repository..."
    git clone https://github.com/Irutingab/Engage_Metrics.git
    cd Engage_Metrics
fi

# Build and run with Docker Compose
echo "🏗️ Building Docker image..."
docker-compose build

echo "▶️ Starting application..."
docker-compose up -d

# Install Nginx if not present
if ! command -v nginx &> /dev/null; then
    echo "🌐 Installing Nginx..."
    apt-get install nginx -y
fi

# Configure Nginx reverse proxy
echo "⚙️ Configuring Nginx..."
cat > /etc/nginx/sites-available/engage-metrics << 'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_read_timeout 86400;
    }
}
EOF

# Enable site
ln -sf /etc/nginx/sites-available/engage-metrics /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx

# Setup firewall
echo "🔒 Configuring firewall..."
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 22/tcp
ufw --force enable

echo "✅ Deployment complete!"
echo "📍 Your app should be accessible at http://$(curl -s ifconfig.me)"
echo ""
echo "Next steps:"
echo "1. Point your domain to this IP address"
echo "2. Run: certbot --nginx -d yourdomain.com (for HTTPS)"
echo "3. Monitor logs: docker-compose logs -f"

# 🚀 Deployment Guide

## Development Deployment

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Virtual environment support
- 2GB RAM minimum
- 1GB free disk space

### Step-by-Step Setup

#### 1. Environment Setup
```powershell
# Navigate to project directory
cd "d:\BE Major Project All\my choice\cyber-triage-tool"

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip
```

#### 2. Install Dependencies
```powershell
# Install all required packages
pip install -r requirements.txt

# Verify installation
python -c "import flask; import yaml; print('Dependencies OK')"
```

#### 3. Configuration
```powershell
# Edit configuration (optional)
notepad config\default.yaml

# Key settings to review:
# - app.web.host (default: 127.0.0.1)
# - app.web.port (default: 8000)
# - triage.quick_scan.max_file_size_mb (default: 50)
```

#### 4. Test Installation
```powershell
# Run help command
python .\main.py --help

# Run sanity test
pytest tests\test_sanity.py -v

# Test analyzers
pytest tests\test_analyzers.py -v
```

#### 5. Start Application
```powershell
# Start web interface
python .\main.py --web-interface

# Access at: http://127.0.0.1:8000
```

---

## Production Deployment

### Architecture Overview
```
Internet
    ↓
[Firewall]
    ↓
[Nginx Reverse Proxy] (Port 80/443)
    ↓
[Gunicorn WSGI Server] (Port 8000)
    ↓
[Cyber Triage Application]
    ↓
[PostgreSQL Database] (Optional)
```

### 1. Server Requirements

#### Minimum Specifications
- **CPU**: 2 cores
- **RAM**: 4GB
- **Storage**: 20GB SSD
- **OS**: Windows Server 2019+ or Linux (Ubuntu 20.04+)
- **Network**: Isolated security segment

#### Recommended Specifications
- **CPU**: 4+ cores
- **RAM**: 8GB+
- **Storage**: 50GB+ SSD
- **OS**: Ubuntu 22.04 LTS
- **Network**: Dedicated VLAN

### 2. Production Setup (Linux)

#### Install System Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.10 python3.10-venv python3-pip -y

# Install Nginx
sudo apt install nginx -y

# Install PostgreSQL (optional)
sudo apt install postgresql postgresql-contrib -y

# Install build tools for some Python packages
sudo apt install build-essential libssl-dev libffi-dev python3-dev -y
```

#### Setup Application
```bash
# Create application user
sudo useradd -m -s /bin/bash cyberapp
sudo su - cyberapp

# Clone/copy application
mkdir -p /opt/cyber-triage
cd /opt/cyber-triage

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn  # WSGI server
```

#### Configure Gunicorn
```bash
# Create gunicorn config
cat > gunicorn_config.py << EOF
bind = "127.0.0.1:8000"
workers = 4
worker_class = "eventlet"  # For SocketIO support
timeout = 120
accesslog = "/var/log/cyber-triage/access.log"
errorlog = "/var/log/cyber-triage/error.log"
loglevel = "info"
EOF

# Create log directory
sudo mkdir -p /var/log/cyber-triage
sudo chown cyberapp:cyberapp /var/log/cyber-triage
```

#### Create Systemd Service
```bash
# Create service file
sudo cat > /etc/systemd/system/cyber-triage.service << EOF
[Unit]
Description=Cyber Triage Tool
After=network.target

[Service]
Type=notify
User=cyberapp
Group=cyberapp
WorkingDirectory=/opt/cyber-triage
Environment="PATH=/opt/cyber-triage/venv/bin"
ExecStart=/opt/cyber-triage/venv/bin/gunicorn \
    --config gunicorn_config.py \
    "src.web.app:create_app()[0]"
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable cyber-triage
sudo systemctl start cyber-triage
sudo systemctl status cyber-triage
```

#### Configure Nginx
```bash
# Create Nginx config
sudo cat > /etc/nginx/sites-available/cyber-triage << EOF
server {
    listen 80;
    server_name cyber-triage.yourdomain.com;

    # Redirect to HTTPS
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name cyber-triage.yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/ssl/certs/cyber-triage.crt;
    ssl_certificate_key /etc/ssl/private/cyber-triage.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Logging
    access_log /var/log/nginx/cyber-triage-access.log;
    error_log /var/log/nginx/cyber-triage-error.log;

    # Proxy settings
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Static files
    location /static {
        alias /opt/cyber-triage/src/web/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/cyber-triage /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 3. SSL/TLS Setup

#### Using Let's Encrypt (Free)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot --nginx -d cyber-triage.yourdomain.com

# Auto-renewal is configured automatically
```

#### Using Self-Signed Certificate (Testing)
```bash
# Generate self-signed certificate
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/private/cyber-triage.key \
    -out /etc/ssl/certs/cyber-triage.crt
```

### 4. Database Setup (Optional)

#### PostgreSQL Configuration
```bash
# Create database and user
sudo -u postgres psql << EOF
CREATE DATABASE cyber_triage;
CREATE USER cyberapp WITH PASSWORD 'secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE cyber_triage TO cyberapp;
\q
EOF

# Update application config
# Edit config/default.yaml to add database connection
```

### 5. Security Hardening

#### Firewall Configuration
```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable

# Restrict SSH to specific IPs (recommended)
sudo ufw delete allow 22/tcp
sudo ufw allow from YOUR_IP_ADDRESS to any port 22
```

#### Application Security
```bash
# Update config/default.yaml
# Change SECRET_KEY to random value
python -c "import secrets; print(secrets.token_hex(32))"

# Set secure permissions
chmod 600 config/default.yaml
chmod 700 data/cases
```

#### System Hardening
```bash
# Disable root login
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo systemctl restart sshd

# Enable automatic security updates
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 6. Monitoring & Logging

#### Setup Log Rotation
```bash
# Create logrotate config
sudo cat > /etc/logrotate.d/cyber-triage << EOF
/var/log/cyber-triage/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 cyberapp cyberapp
    sharedscripts
    postrotate
        systemctl reload cyber-triage > /dev/null 2>&1 || true
    endscript
}
EOF
```

#### Health Check Script
```bash
# Create health check
cat > /opt/cyber-triage/healthcheck.sh << EOF
#!/bin/bash
response=\$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/)
if [ \$response -eq 200 ]; then
    echo "OK: Application is running"
    exit 0
else
    echo "ERROR: Application returned \$response"
    exit 1
fi
EOF

chmod +x /opt/cyber-triage/healthcheck.sh

# Add to cron for monitoring
(crontab -l 2>/dev/null; echo "*/5 * * * * /opt/cyber-triage/healthcheck.sh") | crontab -
```

### 7. Backup Strategy

#### Automated Backups
```bash
# Create backup script
cat > /opt/cyber-triage/backup.sh << EOF
#!/bin/bash
BACKUP_DIR="/backup/cyber-triage"
DATE=\$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p \$BACKUP_DIR

# Backup data
tar -czf \$BACKUP_DIR/data_\$DATE.tar.gz data/cases/

# Backup config
tar -czf \$BACKUP_DIR/config_\$DATE.tar.gz config/

# Keep only last 30 days
find \$BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "Backup completed: \$DATE"
EOF

chmod +x /opt/cyber-triage/backup.sh

# Schedule daily backups
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/cyber-triage/backup.sh") | crontab -
```

### 8. Performance Tuning

#### Gunicorn Workers
```python
# Calculate optimal workers
# Formula: (2 x CPU cores) + 1
# For 4 cores: (2 x 4) + 1 = 9 workers

# Update gunicorn_config.py
workers = 9
worker_class = "eventlet"
worker_connections = 1000
```

#### System Limits
```bash
# Increase file descriptors
sudo cat >> /etc/security/limits.conf << EOF
cyberapp soft nofile 65536
cyberapp hard nofile 65536
EOF

# Increase system limits
sudo cat >> /etc/sysctl.conf << EOF
net.core.somaxconn = 1024
net.ipv4.tcp_max_syn_backlog = 2048
EOF

sudo sysctl -p
```

---

## Docker Deployment (Alternative)

### Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn eventlet

# Copy application
COPY . .

# Create data directory
RUN mkdir -p data/cases logs

# Expose port
EXPOSE 8000

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", \
     "--workers", "4", "--worker-class", "eventlet", \
     "src.web.app:create_app()[0]"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  cyber-triage:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./config:/app/config
      - ./logs:/app/logs
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl
    depends_on:
      - cyber-triage
    restart: unless-stopped
```

### Deploy with Docker
```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## Maintenance

### Regular Tasks

#### Daily
- Check application logs
- Monitor disk space
- Review scan results

#### Weekly
- Review security logs
- Update YARA rules
- Check for updates

#### Monthly
- Update dependencies
- Review access logs
- Test backups
- Security audit

### Update Procedure
```bash
# Backup current version
sudo systemctl stop cyber-triage
cp -r /opt/cyber-triage /opt/cyber-triage.backup

# Update code
cd /opt/cyber-triage
git pull  # or copy new files

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Test
pytest tests/ -v

# Restart
sudo systemctl start cyber-triage
sudo systemctl status cyber-triage
```

---

## Troubleshooting

### Common Issues

**Service won't start**
```bash
# Check logs
sudo journalctl -u cyber-triage -n 50

# Check permissions
ls -la /opt/cyber-triage

# Test manually
cd /opt/cyber-triage
source venv/bin/activate
python main.py --web-interface
```

**High memory usage**
```bash
# Check processes
ps aux | grep gunicorn

# Reduce workers in gunicorn_config.py
workers = 2

# Restart service
sudo systemctl restart cyber-triage
```

**Slow scans**
```bash
# Increase file size limit
# Edit config/default.yaml
max_file_size_mb: 100

# Add more workers
# Edit gunicorn_config.py
workers = 8
```

---

## Support

For deployment issues:
1. Check logs in `/var/log/cyber-triage/`
2. Review system logs: `sudo journalctl -xe`
3. Test configuration: `nginx -t`
4. Verify permissions: `ls -la /opt/cyber-triage`

---

**Deployment Complete! 🎉**

# Deployment Guide - Project Portfolio Website

## Overview
This guide covers deploying your Flask portfolio website with Firestore database to production safely and securely.

## Pre-Deployment Checklist

### 1. Firebase Setup
- [x] Create Firebase project
- [x] Enable Firestore database
- [x] Configure Firebase authentication (optional)
- [ ] Create service account key for production
- [ ] Set up Firebase security rules

### 2. Environment Variables Setup

#### Required Environment Variables:
```bash
# Flask Configuration
SESSION_SECRET=generate-a-secure-random-key-32-chars-minimum
FLASK_ENV=production

# Firebase Configuration
FIREBASE_API_KEY=your-firebase-api-key
FIREBASE_PROJECT_ID=your-firebase-project-id
FIREBASE_APP_ID=your-firebase-app-id

# Admin Credentials (CHANGE THESE!)
ADMIN_USERNAME=your-secure-admin-username
ADMIN_PASSWORD=your-very-secure-admin-password

# Google Service Account (for production)
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

### 3. Security Checklist

#### Admin Credentials:
- [ ] Change default admin username from 'admin'
- [ ] Use strong password (minimum 12 characters, mixed case, numbers, symbols)
- [ ] Consider implementing 2FA for admin access

#### Session Security:
- [ ] Generate secure SESSION_SECRET (use: `python -c "import secrets; print(secrets.token_hex(32))"`)
- [ ] Set FLASK_ENV=production
- [ ] Ensure HTTPS is enabled

#### Firebase Security:
- [ ] Configure Firestore security rules
- [ ] Restrict API key usage to your domain
- [ ] Use service account for server-side operations

## Replit Deployment

### 1. Configure Environment Variables in Replit
1. Go to your Repl
2. Click on "Secrets" tab (lock icon)
3. Add all required environment variables listed above

### 2. Custom Domain Setup
1. Purchase your domain
2. In Replit, go to your Repl
3. Click on "Webview" tab
4. Click "Connect Domain"
5. Follow instructions to configure DNS

### 3. Replit Deployment Configuration
Your `.replit` file should contain:
```toml
run = "gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app"

[deployment]
run = ["sh", "-c", "gunicorn --bind 0.0.0.0:5000 main:app"]
deploymentTarget = "cloudrun"
```

## Production Deployment (VPS/Cloud)

### 1. Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx certbot python3-certbot-nginx -y

# Create application user
sudo useradd -m -s /bin/bash portfolio
sudo usermod -aG sudo portfolio
```

### 2. Application Deployment
```bash
# Switch to app user
sudo su - portfolio

# Clone repository
git clone <your-repo-url> /home/portfolio/app
cd /home/portfolio/app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your production values
nano .env
```

### 3. Gunicorn Configuration
Create `/home/portfolio/app/gunicorn.conf.py`:
```python
bind = "127.0.0.1:5000"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True
```

### 4. Systemd Service
Create `/etc/systemd/system/portfolio.service`:
```ini
[Unit]
Description=Portfolio Flask App
After=network.target

[Service]
User=portfolio
Group=portfolio
WorkingDirectory=/home/portfolio/app
Environment="PATH=/home/portfolio/app/venv/bin"
EnvironmentFile=/home/portfolio/app/.env
ExecStart=/home/portfolio/app/venv/bin/gunicorn -c gunicorn.conf.py main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

### 5. Nginx Configuration
Create `/etc/nginx/sites-available/portfolio`:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static {
        alias /home/portfolio/app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### 6. SSL Certificate
```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Enable services
sudo systemctl enable portfolio
sudo systemctl start portfolio
sudo systemctl enable nginx
```

## Firebase Security Rules

### Firestore Rules (`firestore.rules`):
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Allow read access to projects for all users
    match /projects/{projectId} {
      allow read: if true;
      // Only allow admin to write (implement admin token verification)
      allow write: if request.auth != null && request.auth.token.admin == true;
    }
  }
}
```

## Monitoring and Maintenance

### 1. Log Monitoring
```bash
# View application logs
sudo journalctl -u portfolio -f

# View nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 2. Backup Strategy
```bash
# Create backup script for Firestore
gcloud firestore export gs://your-backup-bucket/$(date +%Y-%m-%d)
```

### 3. Updates
```bash
# Update application
cd /home/portfolio/app
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart portfolio
```

## Security Best Practices

1. **Regular Updates**: Keep system and dependencies updated
2. **Firewall**: Configure UFW or iptables
3. **Monitoring**: Set up fail2ban for intrusion prevention
4. **Backups**: Regular database and code backups
5. **SSL**: Always use HTTPS in production
6. **Environment Variables**: Never commit secrets to git
7. **Admin Access**: Use VPN or IP restrictions for admin panel

## Troubleshooting

### Common Issues:
1. **Firestore Connection**: Check service account permissions
2. **Admin Login**: Verify environment variables are set
3. **Static Files**: Ensure nginx can read static directory
4. **SSL Issues**: Check certificate renewal with certbot

### Debug Commands:
```bash
# Check service status
sudo systemctl status portfolio

# Check logs
sudo journalctl -u portfolio --since "1 hour ago"

# Test Firestore connection
python3 -c "from models import Project; print(Project.get_all())"
```
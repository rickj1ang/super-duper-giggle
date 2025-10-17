# Deployment Guide

This guide explains how to deploy the crawler on your server using the pre-built Docker image from GitHub Container Registry (GHCR).

## Prerequisites

- Docker and Docker Compose installed on your server
- Access to the GitHub repository (for pulling the image)

## Authentication with GHCR

The crawler image is stored in GitHub Container Registry. You have two options for authentication:

### Option 1: Using GitHub Token (Recommended)

1. Create a GitHub Personal Access Token with `read:packages` permission
2. Login to GHCR on your server:

```bash
echo $GITHUB_TOKEN | docker login ghcr.io -u rickj1ang --password-stdin
```

### Option 2: Using Docker Login (Interactive)

```bash
docker login ghcr.io
# Enter your GitHub username and Personal Access Token
```

## Deployment

### 1. Clone the Repository

```bash
git clone https://github.com/rickj1ang/super-duper-giggle.git
cd super-duper-giggle
```

### 2. Create Environment File

Create a `.env` file with your configuration:

```bash
cp .env.example .env
```

Edit the `.env` file with your desired settings:

```env
TARGET_URL=https://your-target-website.com
STEALTH_TEST=true
TIMEOUT=30
LANGUAGE=en-US
TIMEZONE=America/New_York
WINDOW_WIDTH=1920
WINDOW_HEIGHT=1080
```

### 3. Pull and Run the Latest Image

```bash
# Pull the latest image
docker-compose -f docker/compose.prod.yaml pull

# Run the crawler
docker-compose -f docker/compose.prod.yaml up
```

### 4. Check Output

The crawler will save its output in the `data/` directory:
- HTML files: `data/html/`
- Screenshots: `data/screenshots/`

## Scheduled Execution

### Using Cron Job

To run the crawler daily at 2 AM, add this to your crontab:

```bash
# Edit crontab
crontab -e

# Add this line (adjust the path to your project)
0 2 * * * cd /path/to/super-duper-giggle && docker-compose -f docker/compose.prod.yaml up >> /var/log/crawler.log 2>&1
```

### Using Systemd Timer (Alternative)

1. Create a service file `/etc/systemd/system/crawler.service`:

```ini
[Unit]
Description=Web Crawler
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
WorkingDirectory=/path/to/super-duper-giggle
ExecStart=/usr/bin/docker-compose -f docker/compose.prod.yaml up
User=your-username
```

2. Create a timer file `/etc/systemd/system/crawler.timer`:

```ini
[Unit]
Description=Run crawler daily at 2 AM
Requires=crawler.service

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

3. Enable and start the timer:

```bash
sudo systemctl enable crawler.timer
sudo systemctl start crawler.timer
```

## Updating the Crawler

When a new version is pushed to the main branch, GitHub Actions automatically builds and pushes a new image. To update your deployment:

```bash
cd /path/to/super-duper-giggle
docker-compose -f docker/compose.prod.yaml pull
# The next run will use the updated image
```

## Monitoring

### Check Container Logs

```bash
docker-compose -f docker/compose.prod.yaml logs crawler
```

### Check Cron Job Logs

```bash
tail -f /var/log/crawler.log
```

### Check Systemd Timer Status

```bash
sudo systemctl status crawler.timer
sudo journalctl -u crawler.service
```

## Troubleshooting

### Image Pull Issues

If you get authentication errors when pulling the image:

```bash
# Re-authenticate with GHCR
docker login ghcr.io

# Or use token method
echo $GITHUB_TOKEN | docker login ghcr.io -u rickj1ang --password-stdin
```

### Container Startup Issues

Check if Chrome service is healthy:

```bash
docker-compose -f docker/compose.prod.yaml ps
```

If Chrome is not healthy, check its logs:

```bash
docker-compose -f docker/compose.prod.yaml logs chrome
```

### Permission Issues

Ensure the `data` directory has proper permissions:

```bash
sudo chown -R $USER:$USER data/
chmod -R 755 data/
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `TARGET_URL` | `https://example.com` | URL to crawl |
| `STEALTH_TEST` | `false` | Enable stealth mode testing |
| `TIMEOUT` | `30` | Page load timeout in seconds |
| `LANGUAGE` | `en-US` | Browser language setting |
| `TIMEZONE` | `America/New_York` | System timezone |
| `WINDOW_WIDTH` | `1920` | Browser window width |
| `WINDOW_HEIGHT` | `1080` | Browser window height |

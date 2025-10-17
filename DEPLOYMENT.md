# Deployment Guide

This guide explains how to deploy the crawler on your server using the pre-built Docker image from GitHub Container Registry (GHCR).

## Prerequisites

- Docker and Docker Compose installed on your server

## Public Repository Access

The crawler image is stored in GitHub Container Registry as a public repository, so **no authentication is required** to pull the image. You can directly pull and run the container without any login setup.

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

# Proxy Configuration (Optional - for bypassing IP blocks)
PROXY_ENABLED=false
PROXY_SERVER=socks5://your-proxy-server:1080
PROXY_USERNAME=your-proxy-username
PROXY_PASSWORD=your-proxy-password
```

### 3. Create Data Directory and Run

```bash
# Create the data directory for output files
mkdir -p data

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

Since the repository is public, you should not encounter authentication errors. If you do see pull issues:

```bash
# Try pulling the image directly
docker pull ghcr.io/rickj1ang/super-duper-giggle/crawler:latest

# Check if the image exists
docker images | grep crawler
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

## Quick Start Commands

For a fast test run on your server:

```bash
# 1. Clone and setup
git clone https://github.com/rickj1ang/super-duper-giggle.git
cd super-duper-giggle

# 2. Create data directory (IMPORTANT!)
mkdir -p data

# 3. Configure your target URL
echo "TARGET_URL=https://your-website.com" > .env

# 4. Run the crawler
docker-compose -f docker/compose.prod.yaml up
```

## Enhanced Stealth Features

The crawler now includes comprehensive stealth capabilities to bypass bot detection:

### Automatic Stealth Techniques
- **WebDriver masking**: Hides automation indicators
- **Chrome runtime simulation**: Mimics real browser behavior  
- **Hardware fingerprinting**: Realistic CPU, memory, and screen properties
- **API spoofing**: Battery, connection, and permissions APIs
- **Canvas/WebGL masking**: Prevents fingerprinting through graphics
- **Human-like behavior**: Random mouse movements and scrolling patterns

### Proxy Support for IP Blocking

If your server IP is blocked by the target website, you can use a proxy:

```env
# Enable proxy support
PROXY_ENABLED=true
PROXY_SERVER=socks5://your-residential-proxy:1080
PROXY_USERNAME=your-username
PROXY_PASSWORD=your-password
```

**Supported proxy formats:**
- `socks5://proxy:1080`
- `http://proxy:8080`
- `https://proxy:8080`

### Troubleshooting Bot Detection

If you're still getting blocked after enabling enhanced stealth:

1. **Try stealth test first:**
   ```env
   STEALTH_TEST=true
   ```
   This will visit `https://bot.sannysoft.com/` to test your stealth effectiveness.

2. **Enable proxy support** (most effective for IP-based blocking):
   ```env
   PROXY_ENABLED=true
   PROXY_SERVER=socks5://your-residential-proxy:1080
   ```

3. **Check the logs** for detection warnings:
   ```bash
   docker-compose -f docker/compose.prod.yaml logs crawler
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
| `PROXY_ENABLED` | `false` | Enable proxy support |
| `PROXY_SERVER` | - | Proxy server URL |
| `PROXY_USERNAME` | - | Proxy authentication username |
| `PROXY_PASSWORD` | - | Proxy authentication password |

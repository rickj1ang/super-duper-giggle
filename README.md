# Web Crawler with Docker

A stealth web crawler built with Python, Selenium, and Docker. The crawler uses a remote Chrome WebDriver to navigate websites, apply stealth techniques to avoid detection, and save HTML content and screenshots.

## Features

- **Stealth Mode**: Advanced bot detection evasion techniques
- **Dockerized**: Easy deployment with Docker Compose
- **Remote WebDriver**: Uses Selenium Grid for scalable crawling
- **CI/CD Ready**: Automated builds with GitHub Actions
- **Production Ready**: Pre-built images available on GitHub Container Registry (public access)

## Quick Start

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rickj1ang/super-duper-giggle.git
   cd super-duper-giggle
   ```

2. **Start the services:**
   ```bash
   cd docker
   docker-compose up
   ```

3. **Check output:**
   The crawler saves HTML and screenshots in the `data/` directory.

### Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed server deployment instructions.

**Quick deployment (no authentication required):**
```bash
# Pull the latest image (public repository)
docker-compose -f docker/compose.prod.yaml pull

# Run the crawler
docker-compose -f docker/compose.prod.yaml up
```

## Configuration

Copy `.env.example` to `.env` and modify the settings:

```env
TARGET_URL=https://your-target-website.com
STEALTH_TEST=true
TIMEOUT=30
LANGUAGE=en-US
TIMEZONE=America/New_York
WINDOW_WIDTH=1920
WINDOW_HEIGHT=1080
```

## Architecture

### Services

- **Chrome**: Selenium standalone Chrome container
- **Crawler**: Python application that connects to Chrome via WebDriver

### CI/CD Pipeline

The project uses GitHub Actions for automated builds:

1. **Trigger**: Push to main branch
2. **Build**: Docker image for linux/amd64 platform
3. **Push**: Image to GitHub Container Registry (GHCR)
4. **Deploy**: Pull latest image on your server

### Scheduled Execution

For daily automated crawling, set up a cron job on your server:

```bash
# Run daily at 2 AM
0 2 * * * cd /path/to/super-duper-giggle && docker-compose -f docker/compose.prod.yaml up
```

## Project Structure

```
├── crawler/                 # Crawler application
│   ├── Dockerfile          # Crawler image definition
│   ├── requirements.txt    # Python dependencies
│   ├── entrypoint.sh       # Container entrypoint
│   └── src/                # Source code
│       ├── crawler.py      # Main crawler logic
│       ├── config.py       # Configuration settings
│       └── stealth.py      # Stealth techniques
├── docker/                 # Docker configurations
│   ├── compose.yaml        # Development compose file
│   └── compose.prod.yaml   # Production compose file
├── data/                   # Output directory (gitignored)
│   ├── html/              # Saved HTML files
│   └── screenshots/       # Screenshot files
├── .github/workflows/      # GitHub Actions
│   └── build-and-push.yml # CI/CD workflow
└── DEPLOYMENT.md          # Deployment guide
```

## Development

### Local Testing

1. **Start Chrome service:**
   ```bash
   cd docker
   docker-compose up chrome -d
   ```

2. **Run crawler locally:**
   ```bash
   cd crawler
   python -m src.crawler
   ```

3. **Test stealth mode:**
   Set `STEALTH_TEST=true` in your environment.

### Adding Features

1. Modify the crawler code in `crawler/src/`
2. Test locally with `docker-compose up`
3. Push to main branch
4. GitHub Actions will automatically build and push the new image

## Monitoring

### Container Logs
```bash
docker-compose -f docker/compose.prod.yaml logs crawler
```

### Health Checks
```bash
docker-compose -f docker/compose.prod.yaml ps
```

### Output Files
Check the `data/` directory for:
- `html/`: Raw HTML content
- `screenshots/`: Visual captures

## Troubleshooting

### Common Issues

1. **Chrome service not starting:**
   - Check available memory (Chrome needs ~2GB)
   - Verify port 4444 is available

2. **Authentication errors:**
   - Ensure you're logged into GHCR: `docker login ghcr.io`
   - Check your GitHub token has `read:packages` permission

3. **Permission issues:**
   - Ensure `data/` directory is writable
   - Check file ownership: `sudo chown -R $USER:$USER data/`

### Getting Help

- Check [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions
- Review container logs for error messages
- Ensure all environment variables are properly set

## License

This project is for educational and research purposes. Please respect website terms of service and robots.txt files when crawling.

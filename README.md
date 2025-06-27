# Anthropic Engineering RSS Feed Generator

This script generates an RSS feed for Anthropic's engineering blog posts using Playwright to scrape the client-side rendered content.

Feed URL: https://raw.githubusercontent.com/conoro/anthropic-engineering-rss-feed/main/anthropic_engineering_rss.xml

## Features

- **Client-side rendering support**: Uses Playwright to handle JavaScript-rendered content
- **Proper date parsing**: Extracts and formats publication dates with timezone support
- **RSS compliance**: Includes GUID elements and atom:link for better interoperability
- **Reverse chronological order**: Articles sorted newest first
- **Error handling**: Robust error handling for missing elements
- **Automated updates**: GitHub Action runs hourly to keep the feed current

## Setup

### Local Usage

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:
```bash
playwright install
```

3. Run the main script:
```bash
python anthropic_rss.py
```

### GitHub Action Setup

1. Fork this repository to your GitHub account

2. Update the RSS feed URL in `anthropic_rss.py`:
   - Replace `YOUR_USERNAME/YOUR_REPO` with your actual GitHub username and repository name
   - The URL should point to: `https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/anthropic_engineering_rss.xml`

3. Enable GitHub Actions in your repository settings

4. The action will automatically:
   - Run every hour
   - Generate a fresh RSS feed
   - Commit and push updates to the repository
   - Make the RSS feed available at the raw GitHub URL

### Accessing the RSS Feed

Once set up, your RSS feed will be available at:
```
https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/anthropic_engineering_rss.xml
```

You can subscribe to this URL in any RSS reader.

## Manual Triggering

You can manually trigger the RSS generation by:
- Going to the "Actions" tab in your GitHub repository
- Selecting "Generate Anthropic Engineering RSS Feed"
- Clicking "Run workflow"

## Usage

Run the main script:
```bash
python anthropic_rss.py
```

The script will generate an `anthropic_engineering_rss.xml` file containing the RSS feed of all engineering blog posts from Anthropic.

## Output

The generated RSS feed includes:
- Post titles
- Post URLs  
- Publication dates (properly formatted)
- GUID elements for unique identification
- Descriptions (same as titles)
- Proper RSS metadata and atom:link elements

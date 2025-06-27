import asyncio
from datetime import datetime, timezone
from feedgen.feed import FeedGenerator
from playwright.async_api import async_playwright
import os
import re
from dateutil import parser as date_parser

class AnthropicRSSGenerator:
    def __init__(self):
        self.base_url = "https://www.anthropic.com/engineering"

    def parse_date(self, date_text):
        """Parse date text and return a datetime object with timezone"""
        try:
            # Clean up the date text
            date_text = date_text.strip()
            
            # Try to parse the date
            parsed_date = date_parser.parse(date_text)
            
            # If no timezone info, assume UTC
            if parsed_date.tzinfo is None:
                parsed_date = parsed_date.replace(tzinfo=timezone.utc)
            
            return parsed_date
        except Exception as e:
            print(f"Error parsing date '{date_text}': {e}")
            # Return current date as fallback with UTC timezone
            return datetime.now(timezone.utc)

    async def fetch_posts(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(self.base_url)
            
            # Wait for articles to be loaded
            await page.wait_for_selector("div.ArticleList_articles__xFkBH")
            
            # Get all article elements
            articles = await page.query_selector_all("div.ArticleList_articles__xFkBH > div > article")
            
            # Store articles data for sorting
            articles_data = []
            
            for article in articles:
                try:
                    # Get title
                    title_element = await article.query_selector("a > div.ArticleList_content__cqKil > h3")
                    title = await title_element.text_content()
                    
                    # Get URL
                    link_element = await article.query_selector("a")
                    url = await link_element.get_attribute("href")
                    if not url.startswith('http'):
                        url = f"https://www.anthropic.com{url}"
                    
                    # Get date
                    date_element = await article.query_selector("a > div.ArticleList_content__cqKil > div")
                    date_text = await date_element.text_content()
                    parsed_date = self.parse_date(date_text)
                    
                    articles_data.append({
                        'title': title,
                        'url': url,
                        'date': parsed_date,
                        'date_text': date_text
                    })
                    
                    print(f"Found: {title} - {date_text}")
                    
                except Exception as e:
                    print(f"Error processing article: {e}")
            
            # Sort articles by date (newest first)
            articles_data.sort(key=lambda x: x['date'], reverse=True)
            
            await browser.close()
            return articles_data

    def create_feed(self):
        """Create a fresh feed instance"""
        feed = FeedGenerator()
        feed.title('Anthropic Engineering Blog')
        feed.link(href=self.base_url, rel='alternate')
        feed.description('Latest engineering posts from Anthropic')
        feed.language('en')
        
        # Add atom:link with rel="self" for better interoperability
        # This should be updated to match your actual GitHub Pages URL
        feed.link(href='https://raw.githubusercontent.com/conoro/anthropic-engineering-rss-feed/main/anthropic_engineering_rss.xml', rel='self')
        
        return feed

    def generate_rss(self, articles_data):
        # Create a fresh feed and add entries in sorted order
        feed = self.create_feed()
        
        for article_data in articles_data:
            entry = feed.add_entry()
            entry.title(article_data['title'])
            entry.link(href=article_data['url'])
            entry.pubDate(article_data['date'])
            entry.description(article_data['title'])
            
            # Add GUID for better interoperability (using the URL as GUID)
            entry.guid(article_data['url'], permalink=True)
            
        # Generate RSS feed content
        rss_content = feed.rss_str(pretty=True)
        return rss_content

async def main():
    generator = AnthropicRSSGenerator()
    articles_data = await generator.fetch_posts()
    rss_content = generator.generate_rss(articles_data)
    
    # Write to file
    with open('anthropic_engineering_rss.xml', 'wb') as f:
        f.write(rss_content)
    
    print("RSS feed generated successfully!")

if __name__ == "__main__":
    asyncio.run(main())

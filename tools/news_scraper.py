"""
News Scraper Tool for fetching AI news from various sources
"""
import requests
import feedparser
from typing import List, Dict, Any
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import config
from utils.logger import get_logger

logger = get_logger(__name__)


class NewsScraper:
    """Tool for scraping AI news from RSS feeds and websites"""
    
    def __init__(self):
        self.sources = config.NEWS_SOURCES
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def fetch_rss_feed(self, url: str, days_back: int = 1) -> List[Dict[str, Any]]:
        """
        Fetch articles from RSS feed
        
        Args:
            url: RSS feed URL
            days_back: Number of days to look back
            
        Returns:
            List of article dictionaries
        """
        articles = []
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        try:
            logger.info(f"Fetching RSS feed: {url}")
            feed = feedparser.parse(url)
            
            for entry in feed.entries:
                # Parse published date
                published = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    published = datetime(*entry.updated_parsed[:6])
                
                # Filter by date
                if published and published < cutoff_date:
                    continue
                
                article = {
                    'title': entry.get('title', 'No title'),
                    'link': entry.get('link', ''),
                    'summary': entry.get('summary', ''),
                    'published': published.strftime('%Y-%m-%d %H:%M') if published else 'Unknown',
                    'source': feed.feed.get('title', url),
                    'content_snippet': self._clean_html(entry.get('summary', ''))[:300]
                }
                
                articles.append(article)
            
            logger.info(f"Fetched {len(articles)} articles from {url}")
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching RSS feed {url}: {e}")
            return []
    
    def fetch_all_sources(self, days_back: int = 1) -> List[Dict[str, Any]]:
        """
        Fetch articles from all configured sources
        
        Args:
            days_back: Number of days to look back
            
        Returns:
            Combined list of articles from all sources
        """
        all_articles = []
        
        for source_url in self.sources:
            articles = self.fetch_rss_feed(source_url, days_back)
            all_articles.extend(articles)
        
        # Sort by date (newest first)
        all_articles.sort(
            key=lambda x: x['published'] if x['published'] != 'Unknown' else '',
            reverse=True
        )
        
        logger.info(f"Total articles fetched from all sources: {len(all_articles)}")
        return all_articles[:config.MAX_NEWS_ARTICLES]
    
    def search_ai_news(self, keywords: List[str] = None) -> List[Dict[str, Any]]:
        """
        Search for AI news with specific keywords
        
        Args:
            keywords: List of keywords to filter by
            
        Returns:
            Filtered list of articles
        """
        if keywords is None:
            keywords = ['AI', 'artificial intelligence', 'machine learning', 'deep learning']
        
        all_articles = self.fetch_all_sources()
        
        # Filter by keywords
        filtered_articles = []
        for article in all_articles:
            text_to_search = f"{article['title']} {article['summary']}".lower()
            if any(keyword.lower() in text_to_search for keyword in keywords):
                filtered_articles.append(article)
        
        logger.info(f"Filtered to {len(filtered_articles)} articles matching keywords")
        return filtered_articles
    
    def _clean_html(self, html_text: str) -> str:
        """Remove HTML tags from text"""
        if not html_text:
            return ""
        
        try:
            soup = BeautifulSoup(html_text, 'html.parser')
            return soup.get_text(strip=True)
        except:
            return html_text
    
    def get_article_content(self, url: str) -> str:
        """
        Fetch full article content from URL (basic implementation)
        
        Args:
            url: Article URL
            
        Returns:
            Article text content
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(['script', 'style']):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:2000]  # Limit to 2000 chars
            
        except Exception as e:
            logger.error(f"Error fetching article content from {url}: {e}")
            return ""


def get_news_scraper() -> NewsScraper:
    """Get instance of NewsScraper"""
    return NewsScraper()

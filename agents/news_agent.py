"""
News Research Agent - Fetches and summarizes AI news
"""
from typing import List, Dict, Any
from tools.news_scraper import NewsScraper
from tools.gemini_tool import get_gemini_api
import config
from utils.logger import get_logger

logger = get_logger(__name__)


class NewsAgent:
    """Agent responsible for discovering and summarizing AI news"""
    
    def __init__(self):
        self.news_scraper = NewsScraper()
        self.gemini = get_gemini_api()
        self.name = "NewsAgent"
    
    def execute(self, days_back: int = 1) -> Dict[str, Any]:
        """
        Execute news research task
        
        Args:
            days_back: Number of days to look back for news
            
        Returns:
            Dictionary with news articles and summaries
        """
        logger.info(f"{self.name}: Starting news research for last {days_back} days")
        
        try:
            # Fetch news articles
            articles = self.news_scraper.fetch_all_sources(days_back=days_back)
            
            if not articles:
                logger.warning(f"{self.name}: No articles found")
                return {
                    'success': False,
                    'articles': [],
                    'summary': "No recent AI news articles found."
                }
            
            logger.info(f"{self.name}: Found {len(articles)} articles")
            
            # Limit to max articles
            articles = articles[:config.MAX_NEWS_ARTICLES]
            
            # Summarize each article using Gemini
            summarized_articles = []
            for i, article in enumerate(articles):
                logger.info(f"{self.name}: Summarizing article {i+1}/{len(articles)}")
                
                # Create prompt for summarization
                summary = self.gemini.summarize_text(
                    f"Title: {article['title']}\n\n{article['summary']}",
                    max_sentences=2
                )
                
                summarized_article = {
                    'title': article['title'],
                    'link': article['link'],
                    'published': article['published'],
                    'source': article['source'],
                    'original_summary': article['summary'][:200],
                    'ai_summary': summary if summary else article['content_snippet'][:150]
                }
                
                summarized_articles.append(summarized_article)
            
            # Generate overall summary
            titles = "\n".join([f"{i+1}. {a['title']}" for i, a in enumerate(summarized_articles)])
            overall_prompt = f"""Based on these AI news headlines from today, write a brief overview (2-3 sentences) of the main trends and topics:

{titles}

Overview:"""
            
            overall_summary = self.gemini.generate_content(overall_prompt, temperature=0.7)
            
            result = {
                'success': True,
                'articles': summarized_articles,
                'article_count': len(summarized_articles),
                'overall_summary': overall_summary if overall_summary else "Multiple AI developments and news today.",
                'agent': self.name
            }
            
            logger.info(f"{self.name}: Successfully completed news research")
            return result
            
        except Exception as e:
            logger.error(f"{self.name}: Error during execution: {e}")
            return {
                'success': False,
                'articles': [],
                'error': str(e),
                'agent': self.name
            }
    
    def get_trending_topics(self, articles: List[Dict[str, Any]]) -> List[str]:
        """Extract trending topics from articles using Gemini"""
        if not articles:
            return []
        
        titles_text = "\n".join([a['title'] for a in articles])
        prompt = f"""From these AI news headlines, extract the top 5 trending topics/themes. 
Return ONLY a comma-separated list of topics:

{titles_text}

Topics:"""
        
        response = self.gemini.generate_content(prompt, temperature=0.3)
        if response:
            topics = [t.strip() for t in response.split(',')]
            return topics[:5]
        return []

"""
Formatter Agent - Formats content for Discord display
"""
from typing import Dict, Any, List
from datetime import datetime
from tools.gemini_tool import get_gemini_api
import config
from utils.logger import get_logger

logger = get_logger(__name__)


class FormatterAgent:
    """Agent responsible for formatting research results for Discord"""
    
    def __init__(self):
        self.gemini = get_gemini_api()
        self.name = "FormatterAgent"
    
    def execute(self, news_data: Dict[str, Any], papers_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute formatting task
        
        Args:
            news_data: News research results
            papers_data: Paper selection results
            
        Returns:
            Dictionary with formatted content
        """
        logger.info(f"{self.name}: Starting content formatting")
        
        try:
            current_date = datetime.now().strftime('%B %d, %Y')
            
            # Generate introduction
            intro = self._generate_introduction(current_date)
            
            # Format news section
            news_section = self._format_news_section(news_data)
            
            # Format papers section
            papers_section = self._format_papers_section(papers_data)
            
            # Format statistics
            stats_section = self._format_statistics(news_data, papers_data)
            
            # Combine all sections
            formatted_content = {
                'date': current_date,
                'introduction': intro,
                'news_section': news_section,
                'papers_section': papers_section,
                'statistics': stats_section,
                'discord_ready': True,
                'agent': self.name
            }
            
            # Generate Discord message format
            formatted_content['discord_message'] = self._create_discord_message(formatted_content)
            
            logger.info(f"{self.name}: Successfully formatted content")
            return {
                'success': True,
                'formatted_content': formatted_content,
                'agent': self.name
            }
            
        except Exception as e:
            logger.error(f"{self.name}: Error during formatting: {e}")
            return {
                'success': False,
                'error': str(e),
                'agent': self.name
            }
    
    def _generate_introduction(self, date: str) -> str:
        """Generate introduction message"""
        intro = self.gemini.generate_intro_message(date)
        
        if not intro:
            intro = f"🤖 Good morning! Here's your daily AI research digest for {date}."
        
        return intro
    
    def _format_news_section(self, news_data: Dict[str, Any]) -> str:
        """Format news articles section"""
        if not news_data.get('success') or not news_data.get('articles'):
            return "```\n📰 AI NEWS TODAY\n```\nNo news articles available today.\n"
        
        articles = news_data['articles']
        
        section = "```\n📰 AI NEWS TODAY\n```\n"
        
        # Add overall summary if available
        if news_data.get('overall_summary'):
            section += f"```yaml\nOverview: {news_data['overall_summary']}\n```\n\n"
        
        section += f"**Top {len(articles)} Stories:**\n\n"
        
        for i, article in enumerate(articles, 1):
            section += "```diff\n"
            section += f"+ Story #{i}\n"
            section += "```\n"
            section += f"**{article['title']}**\n\n"
            section += f"{article['ai_summary']}\n\n"
            section += f"🔗 **Source:** [{article['source']}]({article['link']})\n"
            section += f"📅 **Date:** {article['published']}\n"
            
            if i < len(articles):
                section += "\n" + "─" * 40 + "\n\n"
        
        return section
    
    def _format_papers_section(self, papers_data: Dict[str, Any]) -> str:
        """Format research papers section"""
        if not papers_data.get('success') or not papers_data.get('selected_papers'):
            return "```\n📚 RESEARCH PAPERS\n```\nNo papers selected today.\n"
        
        papers = papers_data['selected_papers']
        
        section = "```\n📚 TOP 10 AI RESEARCH PAPERS\n```\n"
        section += f"```yaml\nSelected from {papers_data.get('total_analyzed', 'many')} recent papers\n```\n\n"
        
        for paper in papers:
            rank = paper.get('rank', '?')
            category = paper.get('category', 'AI')
            
            # Paper header with rank and category
            section += "```ansi\n"
            section += f"\u001b[1;36m#{rank}\u001b[0m | \u001b[1;33m{category}\u001b[0m\n"
            section += "```\n"
            
            # Title
            section += f"📄 **{paper['title']}**\n\n"
            
            # Authors
            section += f"✍️ {paper.get('authors_short', 'Unknown authors')}\n\n"
            
            # Abstract with box
            abstract = paper.get('abstract', '')[:280]
            section += "```\n"
            section += f"{abstract}...\n"
            section += "```\n"
            
            # Selection reason (if available)
            if paper.get('selection_reason'):
                section += f"💡 **Why selected:** {paper['selection_reason']}\n\n"
            
            # Links and metadata
            section += f"🔗 [Read Paper]({paper.get('pdf_url', '#')}) | "
            section += f"📅 {paper.get('published', 'Unknown')}\n"
            
            if rank < len(papers):
                section += "\n" + "━" * 40 + "\n\n"
        
        return section
    
    def _format_statistics(self, news_data: Dict[str, Any], papers_data: Dict[str, Any]) -> str:
        """Format statistics section"""
        news_count = len(news_data.get('articles', []))
        papers_count = len(papers_data.get('selected_papers', []))
        total_papers = papers_data.get('total_analyzed', 0)
        
        section = "```\n📊 TODAY'S STATISTICS\n```\n"
        section += "```yaml\n"
        section += f"News Articles: {news_count}\n"
        section += f"Papers Analyzed: {total_papers}\n"
        section += f"Papers Selected: {papers_count}\n"
        section += "```\n"
        
        return section
    
    def _create_discord_message(self, content: Dict[str, Any]) -> str:
        """Create complete Discord message"""
        message = "```\n"
        message += "══════════════════════════════════════════════════\n"
        message += "          🤖 AI RESEARCH DAILY DIGEST\n"
        message += f"                📅 {content['date']}\n"
        message += "══════════════════════════════════════════════════\n"
        message += "```\n\n"
        
        message += content['introduction'] + "\n\n"
        
        message += "```\n──────────────────────────────────────────────────\n```\n\n"
        message += content['news_section'] + "\n"
        
        message += "```\n──────────────────────────────────────────────────\n```\n\n"
        message += content['papers_section'] + "\n"
        
        message += "```\n──────────────────────────────────────────────────\n```\n\n"
        message += content['statistics'] + "\n"
        
        message += "```\n══════════════════════════════════════════════════\n```\n"
        message += "**Powered by Gemini AI & arXiv**\n"
        
        return message
    
    def create_discord_embeds(self, content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Create Discord embed objects (for future Discord integration)
        
        Returns:
            List of Discord embed dictionaries
        """
        embeds = []
        
        # Main embed
        main_embed = {
            'title': '🤖 AI Research Daily Digest',
            'description': content['introduction'],
            'color': 0x00ff00,  # Green
            'timestamp': datetime.now().isoformat(),
            'footer': {
                'text': 'Powered by Gemini AI & arXiv'
            }
        }
        embeds.append(main_embed)
        
        return embeds

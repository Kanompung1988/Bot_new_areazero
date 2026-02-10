"""
Paper Discovery Agent - Finds new AI/ML research papers
"""
from typing import List, Dict, Any
from tools.arxiv_tool import ArxivTool
import config
from utils.logger import get_logger

logger = get_logger(__name__)


class PaperDiscoveryAgent:
    """Agent responsible for discovering new research papers"""
    
    def __init__(self):
        self.arxiv_tool = ArxivTool()
        self.name = "PaperDiscoveryAgent"
    
    def execute(self, days_back: int = 7, topic: str = None) -> Dict[str, Any]:
        """
        Execute paper discovery task
        
        Args:
            days_back: Number of days to look back for papers (default: 7)
            topic: Optional topic to filter papers
            
        Returns:
            Dictionary with discovered papers
        """
        logger.info(f"{self.name}: Starting paper discovery for last {days_back} days")
        
        try:
            # Fetch papers from arXiv
            papers = self.arxiv_tool.get_recent_papers(
                days_back=days_back,
                max_results=config.MAX_PAPERS_TO_ANALYZE,
                topic=topic
            )
            
            if not papers:
                logger.warning(f"{self.name}: No papers found")
                return {
                    'success': False,
                    'papers': [],
                    'paper_count': 0
                }
            
            logger.info(f"{self.name}: Discovered {len(papers)} papers")
            
            # Add additional metadata
            for paper in papers:
                paper['authors_short'] = self._format_authors(paper['authors'])
                paper['abstract_short'] = paper['abstract'][:300] + "..."
            
            result = {
                'success': True,
                'papers': papers,
                'paper_count': len(papers),
                'agent': self.name
            }
            
            logger.info(f"{self.name}: Successfully completed paper discovery")
            return result
            
        except Exception as e:
            logger.error(f"{self.name}: Error during execution: {e}")
            return {
                'success': False,
                'papers': [],
                'paper_count': 0,
                'error': str(e),
                'agent': self.name
            }
    
    def search_by_topic(self, topic: str, max_results: int = 20) -> List[Dict[str, Any]]:
        """
        Search for papers on a specific topic
        
        Args:
            topic: Research topic to search for
            max_results: Maximum number of results
            
        Returns:
            List of papers
        """
        logger.info(f"{self.name}: Searching papers for topic: {topic}")
        
        try:
            papers = self.arxiv_tool.search_papers(
                query=topic,
                max_results=max_results
            )
            
            for paper in papers:
                paper['authors_short'] = self._format_authors(paper['authors'])
            
            return papers
            
        except Exception as e:
            logger.error(f"{self.name}: Error searching papers: {e}")
            return []
    
    def _format_authors(self, authors: List[str]) -> str:
        """Format author list for display"""
        if not authors:
            return "Unknown"
        
        if len(authors) == 1:
            return authors[0]
        elif len(authors) == 2:
            return f"{authors[0]} and {authors[1]}"
        else:
            return f"{authors[0]} et al."
    
    def filter_by_categories(self, papers: List[Dict[str, Any]], categories: List[str]) -> List[Dict[str, Any]]:
        """Filter papers by arXiv categories"""
        filtered = []
        for paper in papers:
            paper_cats = paper.get('categories', [])
            if any(cat in paper_cats for cat in categories):
                filtered.append(paper)
        return filtered

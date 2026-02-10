"""
arXiv API Tool for fetching AI/ML papers
"""
import arxiv
from datetime import datetime, timedelta
from typing import List, Dict, Any
import config
from utils.logger import get_logger

logger = get_logger(__name__)


class ArxivTool:
    """Tool for searching and fetching papers from arXiv"""
    
    def __init__(self):
        self.client = arxiv.Client()
    
    def get_recent_papers(self, days_back: int = 7, max_results: int = 100, topic: str = None) -> List[Dict[str, Any]]:
        """
        Fetch recent AI/ML papers from arXiv
        
        Args:
            days_back: Number of days to look back (default: 7)
            max_results: Maximum number of papers to fetch
            topic: Optional topic filter (NLP, LLM, CV, Graph, etc.)
            
        Returns:
            List of paper dictionaries
        """
        papers = []
        
        # Topic to category mapping
        topic_map = {
            'nlp': ['cs.CL'],
            'llm': ['cs.CL', 'cs.AI'],
            'cv': ['cs.CV'],
            'computer vision': ['cs.CV'],
            'graph': ['cs.LG', 'cs.AI'],
            'gnn': ['cs.LG'],
            'rl': ['cs.LG', 'cs.AI'],
            'reinforcement learning': ['cs.LG', 'cs.AI'],
        }
        
        # arXiv categories for AI/ML
        if topic:
            topic_lower = topic.lower()
            categories = topic_map.get(topic_lower, ['cs.AI', 'cs.LG'])
        else:
            categories = [
                'cs.AI',  # Artificial Intelligence
                'cs.LG',  # Machine Learning
                'cs.CL',  # Computation and Language (NLP)
                'cs.CV',  # Computer Vision
                'cs.NE',  # Neural and Evolutionary Computing
                'stat.ML',  # Machine Learning (stats)
            ]
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        logger.info(f"Fetching papers from {start_date.date()} to {end_date.date()}")
        
        for category in categories:
            try:
                # Build search query
                query = f"cat:{category}"
                
                # Create search
                search = arxiv.Search(
                    query=query,
                    max_results=max_results // len(categories),
                    sort_by=arxiv.SortCriterion.SubmittedDate,
                    sort_order=arxiv.SortOrder.Descending
                )
                
                # Fetch results
                for result in self.client.results(search):
                    # Check if paper is within date range
                    if result.published.replace(tzinfo=None) < start_date:
                        continue
                    
                    paper = {
                        'id': result.entry_id.split('/')[-1],
                        'title': result.title,
                        'authors': [author.name for author in result.authors],
                        'abstract': result.summary,
                        'published': result.published.strftime('%Y-%m-%d'),
                        'updated': result.updated.strftime('%Y-%m-%d'),
                        'categories': result.categories,
                        'primary_category': result.primary_category,
                        'pdf_url': result.pdf_url,
                        'links': [link.href for link in result.links],
                        'source': 'arxiv'
                    }
                    
                    papers.append(paper)
                    
                logger.info(f"Fetched {len(papers)} papers from category {category}")
                
            except Exception as e:
                logger.error(f"Error fetching papers from category {category}: {e}")
                continue
        
        # Remove duplicates based on paper ID
        unique_papers = {p['id']: p for p in papers}.values()
        papers_list = list(unique_papers)
        
        logger.info(f"Total unique papers fetched: {len(papers_list)}")
        return papers_list
    
    def search_papers(self, query: str, max_results: int = 20) -> List[Dict[str, Any]]:
        """
        Search for specific papers on arXiv
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of paper dictionaries
        """
        papers = []
        
        try:
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            for result in self.client.results(search):
                paper = {
                    'id': result.entry_id.split('/')[-1],
                    'title': result.title,
                    'authors': [author.name for author in result.authors],
                    'abstract': result.summary,
                    'published': result.published.strftime('%Y-%m-%d'),
                    'categories': result.categories,
                    'pdf_url': result.pdf_url,
                    'source': 'arxiv'
                }
                papers.append(paper)
            
            logger.info(f"Found {len(papers)} papers for query: {query}")
            return papers
            
        except Exception as e:
            logger.error(f"Error searching arXiv: {e}")
            return []


def get_arxiv_tool() -> ArxivTool:
    """Get instance of ArxivTool"""
    return ArxivTool()

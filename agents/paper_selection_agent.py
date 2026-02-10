"""
Paper Selection Agent - Selects and ranks the most important papers
"""
from typing import List, Dict, Any
import json
import random
from tools.gemini_tool import get_gemini_api
import config
from utils.logger import get_logger

logger = get_logger(__name__)


class PaperSelectionAgent:
    """Agent responsible for selecting and ranking papers"""
    
    def __init__(self):
        self.gemini = get_gemini_api()
        self.name = "PaperSelectionAgent"
    
    def execute(self, papers: List[Dict[str, Any]], count: int = 10, filter_featured: bool = False) -> Dict[str, Any]:
        """
        Execute paper selection task
        
        Args:
            papers: List of papers to select from
            count: Number of papers to select
            filter_featured: If True, filter out papers that were already featured
            
        Returns:
            Dictionary with selected papers
        """
        logger.info(f"{self.name}: Starting paper selection from {len(papers)} papers")
        
        # Filter out already featured papers if requested
        if filter_featured:
            from database.models import get_db
            db = get_db()
            original_count = len(papers)
            papers = [p for p in papers if not db.paper_was_featured(p.get('id'))]
            filtered_count = original_count - len(papers)
            if filtered_count > 0:
                logger.info(f"{self.name}: Filtered out {filtered_count} already featured papers")
            db.close()
        
        if not papers:
            logger.warning(f"{self.name}: No papers to select from (all may have been featured)")
            return {
                'success': False,
                'selected_papers': [],
                'selection_method': 'none',
                'total_analyzed': 0,
                'agent': self.name
            }
        
        try:
            # If we have fewer papers than needed, return all
            if len(papers) <= count:
                logger.info(f"{self.name}: Fewer papers than requested, returning all")
                return {
                    'success': True,
                    'selected_papers': papers[:count],
                    'selection_method': 'all_available',
                    'agent': self.name
                }
            
            # Use Gemini to rank papers
            selected_papers = self._rank_with_gemini(papers, count)
            
            if not selected_papers:
                # Fallback: random selection
                logger.warning(f"{self.name}: Gemini ranking failed, using random selection")
                selected_papers = self._random_selection(papers, count)
                selection_method = 'random_fallback'
            else:
                selection_method = 'ai_ranked'
            
            # Add categories to papers
            for paper in selected_papers:
                category = self.gemini.categorize_content(
                    paper['title'],
                    paper['abstract'][:500]
                )
                paper['category'] = category.strip() if category else 'Other'
            
            result = {
                'success': True,
                'selected_papers': selected_papers,
                'selection_method': selection_method,
                'total_analyzed': len(papers),
                'agent': self.name
            }
            
            logger.info(f"{self.name}: Successfully selected {len(selected_papers)} papers")
            return result
            
        except Exception as e:
            logger.error(f"{self.name}: Error during execution: {e}")
            # Fallback to random selection
            return {
                'success': True,
                'selected_papers': self._random_selection(papers, count),
                'selection_method': 'random_error_fallback',
                'error': str(e),
                'agent': self.name
            }
    
    def _rank_with_gemini(self, papers: List[Dict[str, Any]], count: int) -> List[Dict[str, Any]]:
        """Use Gemini to rank papers by importance"""
        logger.info(f"{self.name}: Using Gemini to rank papers")
        
        try:
            # Limit papers to analyze to avoid token limits
            papers_to_analyze = papers[:30]
            
            # Get ranking from Gemini
            ranking_response = self.gemini.rank_papers(papers_to_analyze)
            
            if not ranking_response:
                return []
            
            # Parse JSON response
            try:
                # Extract JSON from response (might have extra text)
                json_start = ranking_response.find('[')
                json_end = ranking_response.rfind(']') + 1
                
                if json_start == -1 or json_end == 0:
                    logger.warning(f"{self.name}: No JSON found in Gemini response")
                    return []
                
                json_str = ranking_response[json_start:json_end]
                rankings = json.loads(json_str)
                
                # Extract selected papers based on rankings
                selected = []
                for rank_item in rankings[:count]:
                    paper_idx = rank_item.get('paper_index', 0) - 1  # Convert to 0-based
                    
                    if 0 <= paper_idx < len(papers_to_analyze):
                        paper = papers_to_analyze[paper_idx].copy()
                        paper['rank'] = rank_item.get('rank', 0)
                        paper['selection_reason'] = rank_item.get('reason', 'Selected by AI')
                        selected.append(paper)
                
                logger.info(f"{self.name}: Successfully ranked {len(selected)} papers with Gemini")
                return selected
                
            except (json.JSONDecodeError, ValueError, KeyError) as e:
                logger.error(f"{self.name}: Failed to parse Gemini ranking response: {e}")
                return []
                
        except Exception as e:
            logger.error(f"{self.name}: Error in Gemini ranking: {e}")
            return []
    
    def _random_selection(self, papers: List[Dict[str, Any]], count: int) -> List[Dict[str, Any]]:
        """Randomly select papers (fallback method)"""
        logger.info(f"{self.name}: Using random selection")
        
        selected = random.sample(papers, min(count, len(papers)))
        
        # Add selection metadata
        for i, paper in enumerate(selected):
            paper['rank'] = i + 1
            paper['selection_reason'] = 'Randomly selected'
        
        return selected
    
    def diversity_selection(self, papers: List[Dict[str, Any]], count: int) -> List[Dict[str, Any]]:
        """Select papers ensuring diversity across categories"""
        logger.info(f"{self.name}: Using diversity-based selection")
        
        # Group papers by primary category
        categorized = {}
        for paper in papers:
            cat = paper.get('primary_category', 'unknown')
            if cat not in categorized:
                categorized[cat] = []
            categorized[cat].append(paper)
        
        # Select papers from each category
        selected = []
        papers_per_category = max(1, count // len(categorized))
        
        for category, cat_papers in categorized.items():
            selected.extend(random.sample(
                cat_papers,
                min(papers_per_category, len(cat_papers))
            ))
        
        # Fill remaining slots randomly if needed
        if len(selected) < count:
            remaining = [p for p in papers if p not in selected]
            selected.extend(random.sample(
                remaining,
                min(count - len(selected), len(remaining))
            ))
        
        return selected[:count]

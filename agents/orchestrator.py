"""
Orchestrator Agent - Coordinates all agents to complete the research task
"""
from typing import Dict, Any, Optional, Callable
from datetime import datetime
from agents.news_agent import NewsAgent
from agents.paper_discovery_agent import PaperDiscoveryAgent
from agents.paper_selection_agent import PaperSelectionAgent
from agents.formatter_agent import FormatterAgent
from database.models import get_db
import config
from utils.logger import get_logger

logger = get_logger(__name__)


class Orchestrator:
    """
    Main orchestrator that coordinates all agents to perform daily research
    """
    
    def __init__(self):
        self.name = "Orchestrator"
        
        # Initialize all agents
        self.news_agent = NewsAgent()
        self.paper_discovery_agent = PaperDiscoveryAgent()
        self.paper_selection_agent = PaperSelectionAgent()
        self.formatter_agent = FormatterAgent()
        self.db = get_db()
        
        logger.info(f"{self.name}: Initialized with all agents")
    
    def run_daily_research(self, days_back: int = 1, topic: str = None, progress_callback: Optional[Callable] = None, filter_featured: bool = False) -> Dict[str, Any]:
        """
        Execute complete daily research workflow
        
        Args:
            days_back: Number of days to look back for content
            topic: Optional research topic to focus on
            progress_callback: Optional callback function for progress updates
            filter_featured: If True, filter out papers that were already featured
            
        Returns:
            Dictionary with complete research results
        """
        start_time = datetime.now()
        logger.info(f"{self.name}: Starting daily research workflow")
        logger.info("=" * 70)
        
        results = {
            'success': False,
            'timestamp': start_time.isoformat(),
            'news_data': None,
            'papers_data': None,
            'formatted_content': None,
            'errors': []
        }
        
        try:
            # Step 1: Fetch and analyze news
            logger.info(f"{self.name}: STEP 1/4 - Running News Agent")
            logger.info("-" * 70)
            
            if progress_callback:
                progress_callback({'step': 1, 'status': 'Fetching AI news...', 'progress': 20})
            
            news_data = self.news_agent.execute(days_back=days_back)
            results['news_data'] = news_data
            
            if not news_data['success']:
                logger.warning(f"{self.name}: News agent failed")
                results['errors'].append("News research failed")
            else:
                logger.info(f"{self.name}: ✓ Found {news_data['article_count']} news articles")
            
            # Step 2: Discover research papers
            logger.info(f"{self.name}: STEP 2/4 - Running Paper Discovery Agent")
            logger.info("-" * 70)
            
            if progress_callback:
                progress_callback({'step': 2, 'status': f'Discovering papers... (Found {news_data["article_count"]} news)', 'progress': 40})
            
            discovery_data = self.paper_discovery_agent.execute(days_back=days_back, topic=topic)
            
            if not discovery_data['success']:
                logger.warning(f"{self.name}: Paper discovery failed")
                results['errors'].append("Paper discovery failed")
                discovery_data = {'success': False, 'papers': [], 'paper_count': 0}
            else:
                logger.info(f"{self.name}: ✓ Discovered {discovery_data['paper_count']} papers")
            
            # Step 3: Select top papers
            logger.info(f"{self.name}: STEP 3/4 - Running Paper Selection Agent")
            logger.info("-" * 70)
            
            if progress_callback:
                progress_callback({'step': 3, 'status': f'Analyzing papers... (Found {discovery_data["paper_count"]} papers)', 'progress': 60})
            
            if discovery_data['papers']:
                selection_data = self.paper_selection_agent.execute(
                    papers=discovery_data['papers'],
                    count=config.SELECTED_PAPERS_COUNT,
                    filter_featured=filter_featured
                )
                
                if selection_data['success']:
                    logger.info(f"{self.name}: ✓ Selected {len(selection_data['selected_papers'])} papers "
                              f"using {selection_data['selection_method']} method")
                else:
                    logger.warning(f"{self.name}: Paper selection failed")
                    results['errors'].append("Paper selection failed")
            else:
                selection_data = {'success': False, 'selected_papers': []}
                logger.warning(f"{self.name}: No papers to select from")
            
            results['papers_data'] = selection_data
            
            # Step 4: Format content
            logger.info(f"{self.name}: STEP 4/4 - Running Formatter Agent")
            logger.info("-" * 70)
            
            if progress_callback:
                progress_callback({'step': 4, 'status': f'Formatting results... (Selected {len(selection_data.get("selected_papers", []))} papers)', 'progress': 85})
            
            formatted_result = self.formatter_agent.execute(
                news_data=news_data,
                papers_data=selection_data
            )
            
            if formatted_result['success']:
                results['formatted_content'] = formatted_result['formatted_content']
                logger.info(f"{self.name}: ✓ Content formatted successfully")
                
                # Save featured papers to database if filter was enabled
                if filter_featured and selection_data.get('selected_papers'):
                    for paper in selection_data['selected_papers']:
                        try:
                            self.db.add_paper(paper, featured=True)
                        except Exception as e:
                            logger.warning(f"{self.name}: Failed to save paper {paper.get('id')}: {e}")
                    logger.info(f"{self.name}: ✓ Saved {len(selection_data['selected_papers'])} papers to memory")
            else:
                logger.error(f"{self.name}: Formatting failed")
                results['errors'].append("Content formatting failed")
            
            if progress_callback:
                progress_callback({'step': 4, 'status': 'Completed!', 'progress': 100})
            
            # Mark as success if we got at least some data
            if news_data['success'] or selection_data.get('success'):
                results['success'] = True
            
            # Calculate execution time
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            results['execution_time_seconds'] = execution_time
            
            logger.info("=" * 70)
            logger.info(f"{self.name}: Workflow completed in {execution_time:.2f} seconds")
            logger.info(f"{self.name}: Success: {results['success']}")
            
            if results['errors']:
                logger.warning(f"{self.name}: Errors encountered: {', '.join(results['errors'])}")
            
            return results
            
        except Exception as e:
            logger.error(f"{self.name}: Critical error in workflow: {e}", exc_info=True)
            results['success'] = False
            results['errors'].append(f"Critical error: {str(e)}")
            return results
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        return {
            'orchestrator': self.name,
            'agents': {
                'news_agent': self.news_agent.name,
                'paper_discovery_agent': self.paper_discovery_agent.name,
                'paper_selection_agent': self.paper_selection_agent.name,
                'formatter_agent': self.formatter_agent.name
            },
            'status': 'ready'
        }
    
    def run_test(self) -> Dict[str, Any]:
        """
        Run a quick test of the workflow with minimal data
        """
        logger.info(f"{self.name}: Running test workflow")
        
        # Test with smaller dataset
        test_config = {
            'days_back': 1,
        }
        
        return self.run_daily_research(**test_config)
    
    def save_results(self, results: Dict[str, Any], output_file: Optional[str] = None) -> bool:
        """
        Save results to file
        
        Args:
            results: Results dictionary
            output_file: Path to output file (optional)
            
        Returns:
            Success status
        """
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"output/research_results_{timestamp}.txt"
        
        try:
            import os
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                if results.get('formatted_content'):
                    f.write(results['formatted_content']['discord_message'])
                else:
                    f.write("Research failed to produce formatted content.\n")
                    f.write(f"Errors: {results.get('errors', [])}\n")
            
            logger.info(f"{self.name}: Results saved to {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"{self.name}: Failed to save results: {e}")
            return False

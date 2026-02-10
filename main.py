"""
AI Research Bot - Main Entry Point

This bot performs daily research on AI news and papers, 
and will eventually send results to Discord.
"""
import sys
import argparse
from datetime import datetime

# Fix for Python 3.13+ cgi module removal
import cgi_fix

# Setup logging first
from utils.logger import setup_logging
from utils.helpers import create_directories
from utils.logger import get_logger

# Initialize logging
setup_logging()
logger = get_logger(__name__)

# Import other modules after logging is setup
from agents.orchestrator import Orchestrator
from scheduler.daily_scheduler import create_scheduler
import config


def run_once():
    """Run the research workflow once and exit"""
    logger.info("="*70)
    logger.info("AI RESEARCH BOT - SINGLE RUN MODE")
    logger.info("="*70)
    
    # Create necessary directories
    create_directories()
    
    # Create orchestrator and run
    orchestrator = Orchestrator()
    results = orchestrator.run_daily_research(days_back=1)
    
    # Save results
    if results['success']:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"output/research_{timestamp}.txt"
        orchestrator.save_results(results, output_file)
        
        logger.info("="*70)
        logger.info(f"✓ Research completed successfully!")
        logger.info(f"Results saved to: {output_file}")
        logger.info("="*70)
        
        return 0
    else:
        logger.error("="*70)
        logger.error("✗ Research failed!")
        logger.error(f"Errors: {results.get('errors', [])}")
        logger.error("="*70)
        
        return 1


def run_scheduler():
    """Run the scheduler for daily automated research"""
    logger.info("="*70)
    logger.info("AI RESEARCH BOT - SCHEDULER MODE")
    logger.info("="*70)
    
    # Create necessary directories
    create_directories()
    
    # Create and start scheduler
    scheduler = create_scheduler()
    
    logger.info(f"Bot will run daily at {config.DAILY_RUN_TIME} {config.TIMEZONE}")
    logger.info(f"Next scheduled run: {scheduler.get_next_run_time()}")
    logger.info("Press Ctrl+C to stop")
    logger.info("="*70)
    
    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
        scheduler.stop()


def run_test():
    """Run a quick test of the system"""
    logger.info("="*70)
    logger.info("AI RESEARCH BOT - TEST MODE")
    logger.info("="*70)
    
    create_directories()
    
    # Test Gemini API
    logger.info("Testing Gemini API...")
    from tools.gemini_tool import get_gemini_api
    
    gemini = get_gemini_api()
    test_response = gemini.generate_content("Say 'Gemini API is working!' in one sentence.")
    
    if test_response:
        logger.info(f"✓ Gemini API test successful: {test_response[:100]}")
    else:
        logger.error("✗ Gemini API test failed")
        return 1
    
    # Test orchestrator
    logger.info("Testing orchestrator workflow...")
    orchestrator = Orchestrator()
    results = orchestrator.run_test()
    
    if results['success']:
        logger.info("✓ Orchestrator test successful")
        logger.info(f"  - News articles: {results['news_data'].get('article_count', 0)}")
        logger.info(f"  - Papers analyzed: {results['papers_data'].get('total_analyzed', 0)}")
        logger.info(f"  - Papers selected: {len(results['papers_data'].get('selected_papers', []))}")
        
        return 0
    else:
        logger.error("✗ Orchestrator test failed")
        return 1


def print_status():
    """Print bot configuration and status"""
    print("="*70)
    print("AI RESEARCH BOT - CONFIGURATION")
    print("="*70)
    print(f"Gemini Model: {config.GEMINI_MODEL}")
    print(f"API Key: {config.GEMINI_API_KEY[:20]}..." if config.GEMINI_API_KEY else "API Key: NOT SET")
    print(f"Daily Run Time: {config.DAILY_RUN_TIME} {config.TIMEZONE}")
    print(f"Max News Articles: {config.MAX_NEWS_ARTICLES}")
    print(f"Selected Papers Count: {config.SELECTED_PAPERS_COUNT}")
    print(f"AI Topics: {', '.join(config.AI_TOPICS)}")
    print("="*70)
    print(f"Discord Token: {'SET' if config.DISCORD_TOKEN and config.DISCORD_TOKEN != 'your_discord_bot_token_here' else 'NOT SET'}")
    print(f"Discord Channel: {config.DISCORD_CHANNEL_ID if config.DISCORD_CHANNEL_ID != 'your_channel_id_here' else 'NOT SET'}")
    print("="*70)


def run_discord_bot():
    """Run Discord bot only"""
    logger.info("="*70)
    logger.info("AI RESEARCH BOT - DISCORD BOT MODE")
    logger.info("="*70)
    
    create_directories()
    
    from discord_bot.bot import run_bot
    run_bot()


def run_api_server():
    """Run FastAPI server with Discord bot"""
    logger.info("="*70)
    logger.info("AI RESEARCH BOT - API SERVER MODE")
    logger.info("="*70)
    
    create_directories()
    
    from api import run_api
    run_api(host="0.0.0.0", port=8000)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='AI Research Bot - Daily AI news and papers research',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --once          Run research once and exit
  python main.py --schedule      Run as scheduled service (daily at configured time)
  python main.py --test          Run system tests
  python main.py --status        Show configuration status
  python main.py --discord       Run Discord bot only
  python main.py --api           Run FastAPI server with Discord bot
        """
    )
    
    parser.add_argument('--once', action='store_true',
                       help='Run research once and exit')
    parser.add_argument('--schedule', action='store_true',
                       help='Run as scheduled service')
    parser.add_argument('--test', action='store_true',
                       help='Run system tests')
    parser.add_argument('--status', action='store_true',
                       help='Show configuration status')
    parser.add_argument('--discord', action='store_true',
                       help='Run Discord bot only')
    parser.add_argument('--api', action='store_true',
                       help='Run FastAPI server with Discord bot')
    
    args = parser.parse_args()
    
    # If no arguments, show help
    if not any([args.once, args.schedule, args.test, args.status, args.discord, args.api]):
        parser.print_help()
        return 0
    
    # Execute based on mode
    if args.status:
        print_status()
        return 0
    
    if args.test:
        return run_test()
    
    if args.once:
        return run_once()
    
    if args.schedule:
        run_scheduler()
        return 0
    
    if args.discord:
        run_discord_bot()
        return 0
    
    if args.api:
        run_api_server()
        return 0


if __name__ == '__main__':
    sys.exit(main())

"""
Scheduler module for daily automated research
"""
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import pytz
import config
from agents.orchestrator import Orchestrator
from utils.logger import get_logger

logger = get_logger(__name__)


class DailyScheduler:
    """Scheduler for running daily research tasks"""
    
    def __init__(self):
        self.scheduler = BlockingScheduler(timezone=pytz.timezone(config.TIMEZONE))
        self.orchestrator = Orchestrator()
        self.name = "DailyScheduler"
        
        logger.info(f"{self.name}: Initialized")
    
    def schedule_daily_job(self):
        """Schedule the daily research job"""
        # Parse time from config (format: HH:MM)
        hour, minute = map(int, config.DAILY_RUN_TIME.split(':'))
        
        # Create cron trigger
        trigger = CronTrigger(
            hour=hour,
            minute=minute,
            timezone=pytz.timezone(config.TIMEZONE)
        )
        
        # Add job to scheduler
        self.scheduler.add_job(
            self.run_daily_research,
            trigger=trigger,
            id='daily_research_job',
            name='Daily AI Research Job',
            replace_existing=True
        )
        
        logger.info(f"{self.name}: Scheduled daily job at {config.DAILY_RUN_TIME} {config.TIMEZONE}")
    
    def run_daily_research(self):
        """Execute the daily research workflow"""
        logger.info("="*70)
        logger.info(f"{self.name}: Starting scheduled daily research")
        logger.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("="*70)
        
        try:
            # Run the orchestrator
            results = self.orchestrator.run_daily_research(days_back=1)
            
            if results['success']:
                logger.info(f"{self.name}: ✓ Daily research completed successfully")
                
                # Save results to file
                timestamp = datetime.now().strftime('%Y%m%d')
                output_file = f"output/research_{timestamp}.txt"
                self.orchestrator.save_results(results, output_file)
                
                # TODO: Send to Discord when Discord integration is ready
                self._send_to_discord(results)
                
            else:
                logger.error(f"{self.name}: ✗ Daily research failed")
                logger.error(f"Errors: {results.get('errors', [])}")
                
                # TODO: Send error notification to Discord admin
                
        except Exception as e:
            logger.error(f"{self.name}: Critical error during scheduled run: {e}", exc_info=True)
    
    def _send_to_discord(self, results: dict):
        """
        Send results to Discord (placeholder for future implementation)
        
        Args:
            results: Research results dictionary
        """
        if not results.get('formatted_content'):
            logger.warning(f"{self.name}: No formatted content to send to Discord")
            return
        
        # TODO: Implement Discord sending when Discord bot is ready
        logger.info(f"{self.name}: Discord integration pending - results saved to file")
        
        # Placeholder code for future Discord integration:
        """
        try:
            from discord_bot.sender import send_message
            
            message = results['formatted_content']['discord_message']
            success = send_message(message, channel_id=config.DISCORD_CHANNEL_ID)
            
            if success:
                logger.info(f"{self.name}: ✓ Results sent to Discord")
            else:
                logger.error(f"{self.name}: ✗ Failed to send to Discord")
                
        except Exception as e:
            logger.error(f"{self.name}: Discord send error: {e}")
        """
    
    def start(self):
        """Start the scheduler"""
        logger.info("="*70)
        logger.info(f"{self.name}: Starting scheduler")
        logger.info(f"Next run time: {self.scheduler.get_jobs()[0].next_run_time if self.scheduler.get_jobs() else 'No jobs scheduled'}")
        logger.info("="*70)
        
        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            logger.info(f"{self.name}: Scheduler stopped by user")
        except Exception as e:
            logger.error(f"{self.name}: Scheduler error: {e}", exc_info=True)
    
    def run_now(self):
        """Run the research job immediately (for testing)"""
        logger.info(f"{self.name}: Running job immediately (manual trigger)")
        self.run_daily_research()
    
    def get_next_run_time(self) -> str:
        """Get the next scheduled run time"""
        jobs = self.scheduler.get_jobs()
        if jobs:
            next_run = jobs[0].next_run_time
            return next_run.strftime('%Y-%m-%d %H:%M:%S %Z')
        return "No jobs scheduled"
    
    def stop(self):
        """Stop the scheduler"""
        logger.info(f"{self.name}: Stopping scheduler")
        self.scheduler.shutdown()


def create_scheduler() -> DailyScheduler:
    """Factory function to create and configure scheduler"""
    scheduler = DailyScheduler()
    scheduler.schedule_daily_job()
    return scheduler

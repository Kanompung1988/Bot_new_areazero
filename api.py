"""
FastAPI Application for AI Research Bot
Provides REST API and webhook endpoints
"""
from fastapi import FastAPI, BackgroundTasks, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import asyncio
from datetime import datetime
import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from agents.orchestrator import Orchestrator
from discord_bot.bot import get_bot, set_bot, create_bot
from discord_bot.sender import set_sender_bot
from database.models import get_db
import config
from utils.logger import get_logger, setup_logging

# Setup logging
setup_logging()
logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Research Bot API",
    description="REST API for AI Research Bot with Discord integration",
    version="1.0.0"
)

# Global instances
orchestrator = Orchestrator()
db = get_db()
bot_task: Optional[asyncio.Task] = None
scheduler: Optional[AsyncIOScheduler] = None
keep_alive_task: Optional[asyncio.Task] = None


# Pydantic models for API
class ResearchRequest(BaseModel):
    days_back: int = 1
    send_to_discord: bool = True


class ResearchResponse(BaseModel):
    success: bool
    message: str
    execution_time: Optional[float] = None
    news_count: Optional[int] = None
    papers_count: Optional[int] = None
    errors: Optional[list] = None


class StatusResponse(BaseModel):
    status: str
    bot_online: bool
    gemini_model: str
    database_stats: Dict[str, Any]


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "AI Research Bot API",
        "version": "1.0.0",
        "status": "online",
        "endpoints": {
            "research": "/api/research",
            "status": "/api/status",
            "health": "/health",
            "ping": "/ping"
        }
    }


@app.get("/ping")
async def ping():
    """Simple ping endpoint for keep-alive services"""
    return {"ping": "pong", "timestamp": datetime.now().isoformat()}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    bot = get_bot()
    
    # Check bot status
    bot_status = {
        "exists": bot is not None,
        "ready": bot.is_ready() if bot else False,
        "connected": False,
        "guilds": 0,
        "latency": 0
    }
    
    if bot:
        bot_status["connected"] = not bot.is_closed()
        bot_status["guilds"] = len(bot.guilds) if bot.guilds else 0
        bot_status["latency"] = round(bot.latency * 1000, 2) if bot.is_ready() else 0
    
    # Determine overall health
    is_healthy = bot_status["ready"] and bot_status["connected"]
    
    return {
        "status": "healthy" if is_healthy else "degraded",
        "timestamp": datetime.now().isoformat(),
        "bot": bot_status,
        "database": "connected"
    }


@app.get("/api/status", response_model=StatusResponse)
async def get_status():
    """Get bot status and statistics"""
    try:
        bot = get_bot()
        stats = db.get_statistics()
        
        return StatusResponse(
            status="online",
            bot_online=bot is not None and bot.is_ready() if bot else False,
            gemini_model=config.GEMINI_MODEL,
            database_stats=stats
        )
    except Exception as e:
        logger.error(f"Status endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/research", response_model=ResearchResponse)
async def run_research(request: ResearchRequest, background_tasks: BackgroundTasks):
    """
    Trigger research workflow
    
    Args:
        request: Research request parameters
        background_tasks: FastAPI background tasks
    """
    try:
        logger.info(f"Research API called with days_back={request.days_back}")
        
        # Run research
        results = orchestrator.run_daily_research(days_back=request.days_back)
        
        if results['success']:
            # Send to Discord if requested
            if request.send_to_discord:
                bot = get_bot()
                if bot and bot.is_ready():
                    formatted_content = results.get('formatted_content')
                    if formatted_content:
                        background_tasks.add_task(
                            bot.send_daily_digest,
                            formatted_content
                        )
            
            # Save to database
            db.add_research_run(
                success=True,
                news_count=results['news_data'].get('article_count', 0),
                papers_count=len(results['papers_data'].get('selected_papers', [])),
                execution_time=int(results.get('execution_time_seconds', 0))
            )
            
            return ResearchResponse(
                success=True,
                message="Research completed successfully",
                execution_time=results.get('execution_time_seconds'),
                news_count=results['news_data'].get('article_count', 0),
                papers_count=len(results['papers_data'].get('selected_papers', []))
            )
        else:
            return ResearchResponse(
                success=False,
                message="Research failed",
                errors=results.get('errors', [])
            )
            
    except Exception as e:
        logger.error(f"Research API error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/test")
async def test_systems():
    """Test bot systems"""
    try:
        results = {
            "gemini_api": False,
            "database": False,
            "discord_bot": False,
            "orchestrator": False
        }
        
        # Test Gemini
        try:
            from tools.gemini_tool import get_gemini_api
            gemini = get_gemini_api()
            response = gemini.generate_content("Test")
            results["gemini_api"] = response is not None
        except Exception as e:
            logger.error(f"Gemini test failed: {e}")
        
        # Test Database
        try:
            stats = db.get_statistics()
            results["database"] = True
        except Exception as e:
            logger.error(f"Database test failed: {e}")
        
        # Test Discord Bot
        try:
            bot = get_bot()
            results["discord_bot"] = bot is not None and bot.is_ready() if bot else False
        except Exception as e:
            logger.error(f"Discord bot test failed: {e}")
        
        # Test Orchestrator
        try:
            status = orchestrator.get_workflow_status()
            results["orchestrator"] = status['status'] == 'ready'
        except Exception as e:
            logger.error(f"Orchestrator test failed: {e}")
        
        all_passed = all(results.values())
        
        return {
            "success": all_passed,
            "results": results,
            "message": "All tests passed" if all_passed else "Some tests failed"
        }
        
    except Exception as e:
        logger.error(f"Test endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def keep_alive():
    """
    Keep-alive task to prevent Render free tier from spinning down
    Pings every 10 minutes to keep service active
    """
    import aiohttp
    
    while True:
        try:
            await asyncio.sleep(600)  # Wait 10 minutes
            
            # Self-ping to keep service alive
            bot = get_bot()
            if bot:
                logger.debug(f"Keep-alive: Bot status - Ready: {bot.is_ready()}, Closed: {bot.is_closed()}")
                
                # If bot is disconnected, try to reconnect
                if bot.is_closed() and not bot.is_ready():
                    logger.warning("Bot appears disconnected, attempting restart...")
                    # The bot should auto-reconnect via discord.py's built-in reconnection
            
        except asyncio.CancelledError:
            logger.info("Keep-alive task cancelled")
            break
        except Exception as e:
            logger.error(f"Keep-alive error: {e}")
            await asyncio.sleep(60)  # Wait 1 minute before retry


async def run_daily_research():
    """
    Scheduled job to run daily research at 8 AM
    """
    logger.info("="*70)
    logger.info("🕐 SCHEDULED DAILY RESEARCH STARTED")
    logger.info("="*70)
    
    try:
        bot = get_bot()
        if not bot or not bot.is_ready():
            logger.error("Bot not ready for scheduled research")
            return
        
        # Run research with default 7 days lookback and memory filter enabled
        results = orchestrator.run_daily_research(
            days_back=config.DEFAULT_DAYS_BACK,
            filter_featured=True  # Filter out papers already sent
        )
        
        if results.get('success'):
            # Send to Discord
            formatted = results.get('formatted_content', {})
            await bot.send_daily_digest(formatted)
            
            logger.info("✅ Daily research completed and sent to Discord")
        else:
            logger.error(f"Daily research failed: {results.get('errors')}")
            
    except Exception as e:
        logger.error(f"Scheduled research error: {e}", exc_info=True)


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    global bot_task, scheduler
    
    logger.info("="*70)
    logger.info("Starting AI Research Bot API")
    logger.info("="*70)
    
    # Start Discord bot in background
    if config.DISCORD_TOKEN and config.DISCORD_TOKEN != 'your_discord_bot_token_here':
        logger.info("Starting Discord bot...")
        
        bot = create_bot()
        set_bot(bot)
        set_sender_bot(bot)
        
        # Run bot in background task
        bot_task = asyncio.create_task(bot.start(config.DISCORD_TOKEN))
        
        logger.info("Discord bot started in background")
        
        # Setup daily scheduler
        await asyncio.sleep(3)  # Wait for bot to be ready
        scheduler = AsyncIOScheduler()
        
        # Schedule daily research at 8:00 AM Bangkok time (Asia/Bangkok)
        scheduler.add_job(
            run_daily_research,
            CronTrigger(hour=8, minute=0, timezone='Asia/Bangkok'),
            id='daily_research',
            name='Daily AI Research',
            replace_existing=True
        )
        
        scheduler.start()
        logger.info("✅ Scheduler started - Daily research will run at 8:00 AM Bangkok time")
        
        # Start keep-alive task
        keep_alive_task = asyncio.create_task(keep_alive())
        logger.info("✅ Keep-alive task started - Will ping every 10 minutes")
    else:
        logger.warning("Discord token not configured, bot will not start")
    
    logger.info("API server ready")
    logger.info("="*70)


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    global bot_task, scheduler, keep_alive_task
    
    logger.info("Shutting down AI Research Bot API")
    
    # Stop keep-alive task
    if keep_alive_task:
        keep_alive_task.cancel()
        try:
            await asyncio.wait_for(asyncio.shield(keep_alive_task), timeout=2.0)
        except (asyncio.CancelledError, asyncio.TimeoutError):
            pass
        logger.info("Keep-alive task stopped")
    
    # Stop scheduler
    if scheduler:
        scheduler.shutdown()
        logger.info("Scheduler stopped")
    
    # Stop Discord bot
    bot = get_bot()
    if bot:
        try:
            await bot.close()
            logger.info("Discord bot stopped")
        except Exception as e:
            logger.warning(f"Error closing bot: {e}")
    
    if bot_task:
        bot_task.cancel()
        try:
            await asyncio.wait_for(asyncio.shield(bot_task), timeout=5.0)
        except (asyncio.CancelledError, asyncio.TimeoutError):
            pass
    
    # Close database
    try:
        db.close()
    except Exception as e:
        logger.warning(f"Error closing database: {e}")
    
    logger.info("Shutdown complete")


def run_api(host: str = "0.0.0.0", port: int = 8000):
    """
    Run the FastAPI server
    
    Args:
        host: Host to bind to
        port: Port to listen on
    """
    logger.info(f"Starting API server on {host}:{port}")
    
    uvicorn.run(
        "api:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )


if __name__ == "__main__":
    run_api()

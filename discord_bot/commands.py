"""
Discord Bot Commands
"""
import discord
from discord.ext import commands
from datetime import datetime
import asyncio
from typing import Optional

from agents.orchestrator import Orchestrator
from database.models import get_db
import config
from utils.logger import get_logger

logger = get_logger(__name__)


class ResearchCommands(commands.Cog):
    """Commands cog for research bot"""
    
    def __init__(self, bot):
        self.bot = bot
        self.orchestrator = Orchestrator()
        self.db = get_db()
        
        # Track running tasks
        self.research_in_progress = False
        
        logger.info("ResearchCommands cog loaded")
    
    @commands.command(name='research', aliases=['r', 'run'])
    @commands.cooldown(1, 300, commands.BucketType.guild)  # 5 minute cooldown
    async def research(self, ctx, days: int = None, *, topic: str = None):
        """
        🔍 Run AI research now
        
        Usage: !research [days] [topic]
        Example: !research 1 NLP
                 !research 3 LLM
                 !research 7
        
        Args:
            days: Number of days to look back (default: 7)
            topic: Research topic (NLP, LLM, CV, Graph, etc.) - optional
        """
        # Check if command is in allowed channel
        if config.DISCORD_COMMAND_CHANNEL_ID:
            allowed_channel = int(config.DISCORD_COMMAND_CHANNEL_ID)
            if ctx.channel.id != allowed_channel:
                await ctx.send(f"❌ Please use this command in <#{allowed_channel}>")
                return
        
        if days is None:
            days = config.DEFAULT_DAYS_BACK
        if self.research_in_progress:
            await ctx.send("⏳ Research already in progress. Please wait...")
            return
        
        if days < 1 or days > 7:
            await ctx.send("❌ Days must be between 1 and 7")
            return
        
        self.research_in_progress = True
        
        try:
            # Create initial progress embed
            topic_text = f" **{topic}**" if topic else " **All Topics**"
            embed = discord.Embed(
                title="🔬 AI Research in Progress",
                description=f"**Timeframe:** Last {days} day(s)\n**Focus:** {topic_text}",
                color=discord.Color.blue(),
                timestamp=datetime.now()
            )
            embed.add_field(name="⏳ Status", value="Initializing...", inline=False)
            embed.add_field(name="📊 Progress", value="▱▱▱▱▱▱▱▱▱▱ 0%", inline=False)
            embed.set_footer(text="This may take 2-3 minutes")
            
            status_msg = await ctx.send(embed=embed)
            
            # Progress bars mapping
            progress_bars = {
                0: "▱▱▱▱▱▱▱▱▱▱ 0%",
                20: "🟦🟦▱▱▱▱▱▱▱▱ 20%",
                40: "🟦🟦🟦🟦▱▱▱▱▱▱ 40%",
                60: "🟦🟦🟦🟦🟦🟦▱▱▱▱ 60%",
                85: "🟦🟦🟦🟦🟦🟦🟦🟦▱▱ 85%",
                100: "🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦 100%"
            }
            
            # Progress callback for real-time updates
            async def update_progress(data):
                try:
                    step = data.get('step', 0)
                    status_text = data.get('status', 'Processing...')
                    progress = data.get('progress', 0)
                    
                    # Get closest progress bar
                    bar = progress_bars.get(progress, progress_bars[0])
                    
                    embed.set_field_at(0, name=f"🔍 Step {step}/4", value=status_text, inline=False)
                    embed.set_field_at(1, name="📊 Progress", value=bar, inline=False)
                    
                    await status_msg.edit(embed=embed)
                except Exception as e:
                    logger.error(f"Progress update error: {e}")
            
            # Create sync wrapper for callback
            import threading
            import queue
            
            progress_queue = queue.Queue()
            
            def sync_callback(data):
                progress_queue.put(data)
            
            # Run orchestrator in thread
            start_time = datetime.now()
            
            async def run_with_progress():
                result = await asyncio.to_thread(
                    self.orchestrator.run_daily_research,
                    days_back=days,
                    topic=topic,
                    progress_callback=sync_callback
                )
                return result
            
            # Start research task
            research_task = asyncio.create_task(run_with_progress())
            
            # Process progress updates
            while not research_task.done():
                try:
                    data = progress_queue.get_nowait()
                    await update_progress(data)
                except queue.Empty:
                    pass
                await asyncio.sleep(0.5)
            
            results = await research_task
            await status_msg.edit(embed=embed)
            results = await research_task
            
            # Get final stats
            news_count = results.get('news_data', {}).get('article_count', 0)
            papers_found = len(results.get('papers_data', {}).get('papers', []))
            selected_count = len(results.get('papers_data', {}).get('selected_papers', []))
            
            if results['success']:
                # Final success embed
                execution_time = (datetime.now() - start_time).total_seconds()
                embed.set_field_at(0, name="✅ Status", value="**Research Completed Successfully!**", inline=False)
                embed.set_field_at(1, name="📊 Progress", value=progress_bars[100], inline=False)
                embed.color = discord.Color.green()
                embed.add_field(
                    name="📈 Summary",
                    value=f"• **News:** {news_count} articles\n"
                          f"• **Papers Found:** {papers_found}\n"
                          f"• **Selected:** {selected_count}\n"
                          f"• **Time:** {execution_time:.1f}s",
                    inline=False
                )
                await status_msg.edit(embed=embed)
                await asyncio.sleep(2)
                
                # Send formatted content
                formatted_content = results.get('formatted_content')
                if formatted_content:
                    message = formatted_content['discord_message']
                    
                    # Split and send
                    chunks = self._split_message(message, 2000)
                    for chunk in chunks:
                        await ctx.send(chunk)
                        await asyncio.sleep(1)
                    
                    # Save to database
                    self.db.add_research_run(
                        success=True,
                        news_count=news_count,
                        papers_count=selected_count,
                        execution_time=int(execution_time)
                    )
                else:
                    await ctx.send("⚠️ Research completed but no formatted content available")
            else:
                # Error embed
                error_msg = ', '.join(results.get('errors', ['Unknown error']))
                embed.set_field_at(0, name="❌ Status", value="**Research Failed**", inline=False)
                embed.set_field_at(1, name="📊 Progress", value="▱▱▱▱▱▱▱▱▱▱ Error", inline=False)
                embed.color = discord.Color.red()
                embed.add_field(name="⚠️ Error", value=error_msg[:1024], inline=False)
                await status_msg.edit(embed=embed)
                
        except Exception as e:
            logger.error(f"Research command error: {e}", exc_info=True)
            await ctx.send(f"❌ Error during research: {str(e)}")
        finally:
            self.research_in_progress = False
    
    @commands.command(name='status', aliases=['s', 'info'])
    async def status(self, ctx):
        """
        📊 Show bot status and statistics
        
        Usage: !status
        """
        try:
            # Get database stats
            stats = self.db.get_statistics()
            
            # Create embed
            embed = discord.Embed(
                title="🤖 AI Research Bot Status",
                description="Multi-agent research bot powered by Gemini AI",
                color=discord.Color.green(),
                timestamp=datetime.now()
            )
            
            # Bot info
            embed.add_field(
                name="🤖 Bot Info",
                value=f"**Status:** Online ✅\n**Model:** {config.GEMINI_MODEL}\n**Prefix:** {config.DISCORD_COMMAND_PREFIX}",
                inline=False
            )
            
            # Statistics
            embed.add_field(
                name="📊 Statistics",
                value=f"**Total Runs:** {stats['total_runs']}\n"
                      f"**Successful:** {stats['successful_runs']}\n"
                      f"**Papers Tracked:** {stats['total_papers']}\n"
                      f"**Featured Papers:** {stats['featured_papers']}\n"
                      f"**Articles Tracked:** {stats['total_articles']}",
                inline=False
            )
            
            # Configuration
            embed.add_field(
                name="⚙️ Configuration",
                value=f"**Daily Run Time:** {config.DAILY_RUN_TIME} {config.TIMEZONE}\n"
                      f"**Max News:** {config.MAX_NEWS_ARTICLES}\n"
                      f"**Selected Papers:** {config.SELECTED_PAPERS_COUNT}",
                inline=False
            )
            
            # Agent status
            agent_status = self.orchestrator.get_workflow_status()
            embed.add_field(
                name="🔧 Agents",
                value=f"✓ News Agent\n✓ Paper Discovery\n✓ Paper Selection\n✓ Formatter",
                inline=False
            )
            
            embed.set_footer(text="Use !help to see all commands")
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Status command error: {e}", exc_info=True)
            await ctx.send(f"❌ Error getting status: {str(e)}")
    
    @commands.command(name='test')
    @commands.has_permissions(administrator=True)
    async def test(self, ctx):
        """
        🧪 Test bot systems (Admin only)
        
        Usage: !test
        """
        await ctx.send("🧪 Running system tests...")
        
        try:
            # Test Gemini API
            from tools.gemini_tool import get_gemini_api
            gemini = get_gemini_api()
            
            test_response = await asyncio.to_thread(
                gemini.generate_content,
                "Say 'Test successful!' in one sentence."
            )
            
            if test_response:
                await ctx.send(f"✅ Gemini API: Working\n```{test_response[:100]}```")
            else:
                await ctx.send("❌ Gemini API: Failed")
                return
            
            # Test database
            stats = self.db.get_statistics()
            await ctx.send(f"✅ Database: Working ({stats['total_runs']} runs recorded)")
            
            # Test orchestrator
            workflow_status = self.orchestrator.get_workflow_status()
            await ctx.send(f"✅ Orchestrator: Ready with {len(workflow_status['agents'])} agents")
            
            await ctx.send("✅ All systems operational!")
            
        except Exception as e:
            logger.error(f"Test command error: {e}", exc_info=True)
            await ctx.send(f"❌ Test failed: {str(e)}")
    
    @commands.command(name='stats')
    async def stats(self, ctx, days: int = 7):
        """
        📈 Show research statistics
        
        Usage: !stats [days]
        Example: !stats 7
        """
        try:
            recent_papers = self.db.get_recent_papers(days=days)
            
            embed = discord.Embed(
                title=f"📈 Last {days} Days Statistics",
                color=discord.Color.blue(),
                timestamp=datetime.now()
            )
            
            embed.add_field(
                name="📚 Papers Featured",
                value=f"{len(recent_papers)} papers",
                inline=True
            )
            
            # Group by category
            categories = {}
            for paper in recent_papers:
                cat = paper.category or 'Other'
                categories[cat] = categories.get(cat, 0) + 1
            
            if categories:
                cat_text = '\n'.join([f"• {k}: {v}" for k, v in sorted(categories.items())])
                embed.add_field(
                    name="📊 By Category",
                    value=cat_text,
                    inline=False
                )
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Stats command error: {e}", exc_info=True)
            await ctx.send(f"❌ Error getting stats: {str(e)}")
    
    @commands.command(name='help_research', aliases=['rhelp'])
    async def help_research(self, ctx):
        """
        ❓ Show detailed help
        
        Usage: !help_research
        """
        embed = discord.Embed(
            title="🤖 AI Research Bot - Commands",
            description="Multi-agent bot for daily AI research with Gemini AI",
            color=discord.Color.purple()
        )
        
        embed.add_field(
            name="!research [days] [topic]",
            value="Run AI research now (alias: !r, !run)\n"
                  "**Examples:**\n"
                  "• `!research` - Default (7 days, all topics)\n"
                  "• `!research 1` - Last 1 day, all topics\n"
                  "• `!research 3 NLP` - Last 3 days, NLP only\n"
                  "• `!research 7 LLM` - Last 7 days, LLM only\n\n"
                  "**Available Topics:**\n"
                  "NLP, LLM, CV (Computer Vision), Graph, GNN, RL (Reinforcement Learning)",
            inline=False
        )
        
        embed.add_field(
            name="!status",
            value="Show bot status and statistics (alias: !s, !info)",
            inline=False
        )
        
        embed.add_field(
            name="!stats [days]",
            value="Show research statistics\nExample: `!stats 7`",
            inline=False
        )
        
        embed.add_field(
            name="!test",
            value="Test bot systems (Admin only)",
            inline=False
        )
        
        embed.add_field(
            name="⏰ Automatic Schedule",
            value=f"Bot runs automatically at **8:00 AM Bangkok time** daily\n"
                  f"• Scheduled Channel: <#{config.DISCORD_CHANNEL_ID}>\n"
                  f"• Command Channel: <#{config.DISCORD_COMMAND_CHANNEL_ID}>",
            inline=False
        )
        
        embed.set_footer(text="Made with ❤️ for AI Research | Powered by Gemini AI")
        
        await ctx.send(embed=embed)
    
    def _split_message(self, message: str, max_length: int = 2000) -> list:
        """Split long message into chunks"""
        chunks = []
        current_chunk = ""
        
        for line in message.split('\n'):
            if len(current_chunk) + len(line) + 1 <= max_length:
                current_chunk += line + '\n'
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = line + '\n'
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks


async def setup(bot):
    """Setup function for loading the cog"""
    await bot.add_cog(ResearchCommands(bot))

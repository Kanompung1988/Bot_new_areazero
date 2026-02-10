"""
Discord Bot Implementation
"""
import discord
from discord.ext import commands
from typing import Optional
import asyncio
import config
from utils.logger import get_logger

logger = get_logger(__name__)


class ResearchBot(commands.Bot):
    """Main Discord Bot class for AI Research Bot"""
    
    def __init__(self):
        # Setup intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        
        # Initialize bot
        super().__init__(
            command_prefix=config.DISCORD_COMMAND_PREFIX,
            intents=intents,
            help_command=commands.DefaultHelpCommand()
        )
        
        self.name = "ResearchBot"
        logger.info(f"{self.name}: Initializing Discord bot")
    
    async def setup_hook(self):
        """Called when bot is setting up"""
        logger.info(f"{self.name}: Setting up bot")
        
        # Load commands
        await self.load_extension('discord_bot.commands')
        
        logger.info(f"{self.name}: Bot setup complete")
    
    async def on_ready(self):
        """Called when bot is ready"""
        logger.info("="*70)
        logger.info(f"{self.name}: Bot is ready!")
        logger.info(f"Logged in as: {self.user.name} (ID: {self.user.id})")
        logger.info(f"Connected to {len(self.guilds)} guild(s)")
        logger.info("="*70)
        
        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="AI Research | !help"
            )
        )
    
    async def on_message(self, message):
        """Called when a message is received"""
        # Ignore messages from the bot itself
        if message.author == self.user:
            return
        
        # Process commands
        await self.process_commands(message)
    
    async def on_command_error(self, ctx, error):
        """Called when a command error occurs"""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("❌ Command not found. Use `!help` to see available commands.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command.")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏰ Command on cooldown. Try again in {error.retry_after:.1f}s")
        else:
            logger.error(f"Command error: {error}", exc_info=True)
            await ctx.send(f"❌ An error occurred: {str(error)}")
    
    async def send_to_channel(self, channel_id: int, content: str = None, embed: discord.Embed = None):
        """
        Send message to a specific channel
        
        Args:
            channel_id: Discord channel ID
            content: Text content
            embed: Discord embed object
            
        Returns:
            True if successful, False otherwise
        """
        try:
            channel = self.get_channel(channel_id)
            
            if not channel:
                logger.error(f"{self.name}: Channel {channel_id} not found")
                return False
            
            await channel.send(content=content, embed=embed)
            logger.info(f"{self.name}: Message sent to channel {channel_id}")
            return True
            
        except Exception as e:
            logger.error(f"{self.name}: Failed to send message: {e}")
            return False
    
    async def send_daily_digest(self, formatted_content: dict):
        """
        Send the daily research digest
        
        Args:
            formatted_content: Formatted content from FormatterAgent
        """
        try:
            if not config.DISCORD_CHANNEL_ID or config.DISCORD_CHANNEL_ID == 'your_channel_id_here':
                logger.warning(f"{self.name}: Channel ID not configured")
                return False
            
            channel_id = int(config.DISCORD_CHANNEL_ID)
            channel = self.get_channel(channel_id)
            
            if not channel:
                logger.error(f"{self.name}: Channel {channel_id} not found")
                return False
            
            # Get the formatted message
            message = formatted_content.get('discord_message', '')
            
            # Discord has 2000 char limit, split if needed
            if len(message) <= 2000:
                await channel.send(message)
            else:
                # Split into chunks
                chunks = self._split_message(message, 2000)
                for chunk in chunks:
                    await channel.send(chunk)
                    await asyncio.sleep(1)  # Avoid rate limiting
            
            logger.info(f"{self.name}: Daily digest sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"{self.name}: Failed to send daily digest: {e}")
            return False
    
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


def create_bot() -> ResearchBot:
    """Factory function to create bot instance"""
    return ResearchBot()


def run_bot():
    """Run the Discord bot"""
    if not config.DISCORD_TOKEN or config.DISCORD_TOKEN == 'your_discord_bot_token_here':
        logger.error("Discord token not configured in .env file")
        print("❌ Error: DISCORD_TOKEN not set in .env file")
        return
    
    logger.info("Starting Discord bot...")
    
    bot = create_bot()
    
    try:
        bot.run(config.DISCORD_TOKEN)
    except discord.LoginFailure:
        logger.error("Invalid Discord token")
        print("❌ Error: Invalid Discord token")
    except Exception as e:
        logger.error(f"Bot error: {e}", exc_info=True)
        print(f"❌ Error: {e}")


# Global bot instance for use in other modules
_bot_instance: Optional[ResearchBot] = None

def get_bot() -> Optional[ResearchBot]:
    """Get the bot instance"""
    return _bot_instance

def set_bot(bot: ResearchBot):
    """Set the bot instance"""
    global _bot_instance
    _bot_instance = bot

"""
Discord Message Sender Module
"""
import discord
from typing import Optional, Dict, Any
import asyncio
import config
from utils.logger import get_logger

logger = get_logger(__name__)


class DiscordSender:
    """Helper class for sending messages to Discord"""
    
    def __init__(self, bot=None):
        self.bot = bot
    
    def set_bot(self, bot):
        """Set the bot instance"""
        self.bot = bot
    
    async def send_message(self, channel_id: int, content: str) -> bool:
        """
        Send a simple text message
        
        Args:
            channel_id: Discord channel ID
            content: Message content
            
        Returns:
            Success status
        """
        if not self.bot:
            logger.error("Bot instance not set")
            return False
        
        try:
            channel = self.bot.get_channel(channel_id)
            
            if not channel:
                logger.error(f"Channel {channel_id} not found")
                return False
            
            # Split if too long
            if len(content) <= 2000:
                await channel.send(content)
            else:
                chunks = self._split_message(content, 2000)
                for chunk in chunks:
                    await channel.send(chunk)
                    await asyncio.sleep(1)
            
            logger.info(f"Message sent to channel {channel_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return False
    
    async def send_embed(self, channel_id: int, embed: discord.Embed) -> bool:
        """
        Send an embed message
        
        Args:
            channel_id: Discord channel ID
            embed: Discord Embed object
            
        Returns:
            Success status
        """
        if not self.bot:
            logger.error("Bot instance not set")
            return False
        
        try:
            channel = self.bot.get_channel(channel_id)
            
            if not channel:
                logger.error(f"Channel {channel_id} not found")
                return False
            
            await channel.send(embed=embed)
            logger.info(f"Embed sent to channel {channel_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send embed: {e}")
            return False
    
    async def send_daily_digest(self, formatted_content: Dict[str, Any]) -> bool:
        """
        Send the daily research digest
        
        Args:
            formatted_content: Formatted content from FormatterAgent
            
        Returns:
            Success status
        """
        if not config.DISCORD_CHANNEL_ID or config.DISCORD_CHANNEL_ID == 'your_channel_id_here':
            logger.warning("Channel ID not configured")
            return False
        
        try:
            channel_id = int(config.DISCORD_CHANNEL_ID)
            message = formatted_content.get('discord_message', '')
            
            return await self.send_message(channel_id, message)
            
        except ValueError:
            logger.error(f"Invalid channel ID: {config.DISCORD_CHANNEL_ID}")
            return False
        except Exception as e:
            logger.error(f"Failed to send daily digest: {e}")
            return False
    
    async def send_error_notification(self, error_message: str) -> bool:
        """
        Send error notification to admins
        
        Args:
            error_message: Error description
            
        Returns:
            Success status
        """
        if not config.DISCORD_CHANNEL_ID or config.DISCORD_CHANNEL_ID == 'your_channel_id_here':
            logger.warning("Channel ID not configured for error notifications")
            return False
        
        try:
            channel_id = int(config.DISCORD_CHANNEL_ID)
            
            embed = discord.Embed(
                title="🚨 Error Alert",
                description=error_message,
                color=discord.Color.red()
            )
            
            return await self.send_embed(channel_id, embed)
            
        except Exception as e:
            logger.error(f"Failed to send error notification: {e}")
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


# Global sender instance
_sender_instance: Optional[DiscordSender] = None

def get_sender() -> DiscordSender:
    """Get or create sender instance"""
    global _sender_instance
    if _sender_instance is None:
        _sender_instance = DiscordSender()
    return _sender_instance

def set_sender_bot(bot):
    """Set bot instance for sender"""
    sender = get_sender()
    sender.set_bot(bot)

"""
Discord Bot Health Check & Configuration Validator
ตรวจสอบ bot configuration และ intents
"""
import asyncio
import discord
from discord.ext import commands
import config
from utils.logger import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)


async def check_bot_health():
    """ตรวจสอบสุขภาพและการตั้งค่าของบอท"""
    print("="*70)
    print("🔍 Discord Bot Health Check")
    print("="*70)
    print()
    
    # Check token
    if not config.DISCORD_TOKEN or config.DISCORD_TOKEN == 'your_discord_bot_token_here':
        print("❌ DISCORD_TOKEN not configured")
        print("   Please set DISCORD_TOKEN in .env file")
        return False
    
    print("✓ Discord token configured")
    
    # Setup intents
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True
    intents.guild_messages = True
    intents.members = True
    
    print()
    print("📋 Configured Intents:")
    print(f"  • message_content: {intents.message_content}")
    print(f"  • guilds: {intents.guilds}")
    print(f"  • guild_messages: {intents.guild_messages}")
    print(f"  • members: {intents.members}")
    print()
    
    # Create bot
    bot = commands.Bot(
        command_prefix=config.DISCORD_COMMAND_PREFIX,
        intents=intents,
        help_command=None
    )
    
    connection_success = False
    
    @bot.event
    async def on_ready():
        nonlocal connection_success
        connection_success = True
        
        print("="*70)
        print("✅ Bot Connected Successfully!")
        print("="*70)
        print()
        print(f"Bot Name: {bot.user.name}")
        print(f"Bot ID: {bot.user.id}")
        print(f"Guilds: {len(bot.guilds)}")
        print()
        
        print("📊 Guild Information:")
        for guild in bot.guilds:
            print(f"  • {guild.name} (ID: {guild.id})")
            print(f"    - Members: {guild.member_count}")
            print(f"    - Channels: {len(guild.channels)}")
        
        print()
        print("🔌 Connection Details:")
        print(f"  • Latency: {bot.latency * 1000:.0f}ms")
        print(f"  • Shard ID: {bot.shard_id}")
        print(f"  • Shard Count: {bot.shard_count if bot.shard_count else 1}")
        
        print()
        print("⚙️ Configuration:")
        print(f"  • Command Prefix: {config.DISCORD_COMMAND_PREFIX}")
        print(f"  • Heartbeat Timeout: {config.DISCORD_HEARTBEAT_TIMEOUT}s")
        print(f"  • Keep-Alive Interval: {config.DISCORD_KEEPALIVE_INTERVAL}s")
        
        # Check required intents in Developer Portal
        print()
        print("="*70)
        print("⚠️  IMPORTANT: Discord Developer Portal Settings")
        print("="*70)
        print()
        print("Please verify these intents are ENABLED in Discord Developer Portal:")
        print("https://discord.com/developers/applications")
        print()
        print("Required Intents:")
        print("  ✓ MESSAGE CONTENT INTENT")
        print("  ✓ SERVER MEMBERS INTENT")
        print("  ○ PRESENCE INTENT (optional)")
        print()
        
        # Test sending a message to configured channel
        if config.DISCORD_CHANNEL_ID and config.DISCORD_CHANNEL_ID != 'your_channel_id_here':
            try:
                channel_id = int(config.DISCORD_CHANNEL_ID)
                channel = bot.get_channel(channel_id)
                
                if channel:
                    print(f"✓ Target channel found: #{channel.name}")
                    
                    # Test permissions
                    permissions = channel.permissions_for(guild.me) if bot.guilds else None
                    if permissions:
                        print()
                        print("📝 Bot Permissions in target channel:")
                        print(f"  • Send Messages: {permissions.send_messages}")
                        print(f"  • Embed Links: {permissions.embed_links}")
                        print(f"  • Attach Files: {permissions.attach_files}")
                        print(f"  • Read Messages: {permissions.read_messages}")
                        print(f"  • Read Message History: {permissions.read_message_history}")
                        
                        if not permissions.send_messages:
                            print()
                            print("⚠️  WARNING: Bot cannot send messages in target channel!")
                            print("   Please check channel permissions")
                else:
                    print(f"⚠️  Target channel not found (ID: {channel_id})")
                    print("   Please check DISCORD_CHANNEL_ID in .env")
            except ValueError:
                print(f"❌ Invalid DISCORD_CHANNEL_ID: {config.DISCORD_CHANNEL_ID}")
        
        print()
        print("="*70)
        print("🎉 Health Check Complete!")
        print("="*70)
        print()
        
        if connection_success:
            print("✅ All checks passed! Bot is ready to run.")
            print()
            print("To start bot:")
            print("  • Quick start: .\\start_with_pm2.ps1")
            print("  • Windows Service: .\\install_service_enhanced.ps1")
            print("  • Docker: docker-compose up -d")
            print("  • Manual: python run_bot.py")
        
        # Close bot after check
        await bot.close()
    
    @bot.event
    async def on_error(event, *args, **kwargs):
        print(f"❌ Error during {event}: {args}")
    
    try:
        print("🔄 Connecting to Discord...")
        print()
        
        # Try to connect with timeout
        await asyncio.wait_for(bot.start(config.DISCORD_TOKEN), timeout=30.0)
        
    except asyncio.TimeoutError:
        print("❌ Connection timeout (30s)")
        print("   Possible causes:")
        print("   • Invalid token")
        print("   • Network/firewall issues")
        print("   • Discord API issues")
        return False
    
    except discord.LoginFailure:
        print("❌ Invalid Discord token")
        print("   Please check DISCORD_TOKEN in .env file")
        return False
    
    except discord.PrivilegedIntentsRequired as e:
        print("❌ Privileged Intents Required!")
        print()
        print("You need to enable these intents in Discord Developer Portal:")
        print("https://discord.com/developers/applications")
        print()
        print("Go to: Bot → Privileged Gateway Intents")
        print("Enable:")
        print("  ✓ MESSAGE CONTENT INTENT")
        print("  ✓ SERVER MEMBERS INTENT")
        print()
        print(f"Error details: {e}")
        return False
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        logger.error("Health check error", exc_info=True)
        return False
    
    finally:
        if not bot.is_closed():
            await bot.close()
    
    return connection_success


if __name__ == "__main__":
    print()
    success = asyncio.run(check_bot_health())
    print()
    
    if not success:
        print("❌ Health check failed")
        print("   Please fix the issues above before running the bot")
        exit(1)
    else:
        exit(0)

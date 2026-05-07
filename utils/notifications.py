"""
Notifications System
Alert users via multiple channels
"""

import logging
import asyncio
from typing import Optional
from enum import Enum

logger = logging.getLogger(__name__)


class NotificationChannel(Enum):
    """Notification channels"""
    TELEGRAM = "telegram"
    DISCORD = "discord"
    EMAIL = "email"
    WEBHOOK = "webhook"


class TelegramNotifier:
    """Send notifications via Telegram"""
    
    def __init__(self, bot_token: str, chat_id: str):
        """Initialize Telegram notifier"""
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
    
    async def send(self, message: str) -> bool:
        """Send message via Telegram"""
        import aiohttp
        
        try:
            url = f"{self.api_url}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        logger.info("✅ Telegram message sent")
                        return True
                    else:
                        logger.error(f"❌ Telegram error: {response.status}")
                        return False
        
        except Exception as e:
            logger.error(f"❌ Error sending Telegram: {e}")
            return False


class DiscordNotifier:
    """Send notifications via Discord"""
    
    def __init__(self, webhook_url: str):
        """Initialize Discord notifier"""
        self.webhook_url = webhook_url
    
    async def send(self, message: str, embed: Optional[dict] = None) -> bool:
        """Send message via Discord webhook"""
        import aiohttp
        
        try:
            payload = {'content': message}
            if embed:
                payload['embeds'] = [embed]
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=payload) as response:
                    if response.status in [200, 204]:
                        logger.info("✅ Discord message sent")
                        return True
                    else:
                        logger.error(f"❌ Discord error: {response.status}")
                        return False
        
        except Exception as e:
            logger.error(f"❌ Error sending Discord: {e}")
            return False


class EmailNotifier:
    """Send notifications via Email"""
    
    def __init__(self, smtp_server: str, sender_email: str, sender_password: str):
        """Initialize Email notifier"""
        self.smtp_server = smtp_server
        self.sender_email = sender_email
        self.sender_password = sender_password
    
    async def send(self, recipient: str, subject: str, message: str) -> bool:
        """Send email"""
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'html'))
            
            with smtplib.SMTP(self.smtp_server, 587) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            logger.info(f"✅ Email sent to {recipient}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Error sending email: {e}")
            return False


class WebhookNotifier:
    """Send notifications via generic webhook"""
    
    def __init__(self, webhook_url: str):
        """Initialize webhook notifier"""
        self.webhook_url = webhook_url
    
    async def send(self, data: dict) -> bool:
        """Send data via webhook"""
        import aiohttp
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=data) as response:
                    if response.status in [200, 201, 204]:
                        logger.info("✅ Webhook notification sent")
                        return True
                    else:
                        logger.error(f"❌ Webhook error: {response.status}")
                        return False
        
        except Exception as e:
            logger.error(f"❌ Error sending webhook: {e}")
            return False


class NotificationManager:
    """Manage all notifications"""
    
    def __init__(self):
        self.notifiers = {}
    
    def add_telegram(self, bot_token: str, chat_id: str):
        """Add Telegram notifier"""
        self.notifiers['telegram'] = TelegramNotifier(bot_token, chat_id)
        logger.info("📱 Telegram notifier configured")
    
    def add_discord(self, webhook_url: str):
        """Add Discord notifier"""
        self.notifiers['discord'] = DiscordNotifier(webhook_url)
        logger.info("💬 Discord notifier configured")
    
    def add_email(self, smtp_server: str, sender_email: str, sender_password: str):
        """Add Email notifier"""
        self.notifiers['email'] = EmailNotifier(smtp_server, sender_email, sender_password)
        logger.info("📧 Email notifier configured")
    
    def add_webhook(self, webhook_url: str):
        """Add Webhook notifier"""
        self.notifiers['webhook'] = WebhookNotifier(webhook_url)
        logger.info("🔗 Webhook notifier configured")
    
    async def notify_all(self, message: str, embed: dict = None):
        """Send notification to all configured channels"""
        tasks = []
        
        if 'telegram' in self.notifiers:
            tasks.append(self.notifiers['telegram'].send(message))
        
        if 'discord' in self.notifiers:
            tasks.append(self.notifiers['discord'].send(message, embed))
        
        if 'webhook' in self.notifiers:
            tasks.append(self.notifiers['webhook'].send({'message': message, 'embed': embed}))
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def notify_trading_signal(self, analysis):
        """Send trading signal notification"""
        message = f"""
<b>🎯 TRADING SIGNAL</b>

<b>Pair:</b> {analysis.pair} ({analysis.timeframe})
<b>Signal:</b> {analysis.signal.value}
<b>Confidence:</b> {analysis.confidence:.1f}%

<b>Entry:</b> {analysis.entry_price:.5f}
<b>Stop Loss:</b> {analysis.stop_loss:.5f}
<b>Take Profit:</b> {analysis.take_profit:.5f}
<b>Risk/Reward:</b> {analysis.risk_reward_ratio:.2f}:1
"""
        
        embed = {
            "title": f"{analysis.signal.value} - {analysis.pair}",
            "description": f"Confidence: {analysis.confidence:.1f}%",
            "fields": [
                {"name": "Entry", "value": f"{analysis.entry_price:.5f}", "inline": True},
                {"name": "Stop Loss", "value": f"{analysis.stop_loss:.5f}", "inline": True},
                {"name": "Take Profit", "value": f"{analysis.take_profit:.5f}", "inline": True},
                {"name": "Risk/Reward", "value": f"{analysis.risk_reward_ratio:.2f}:1", "inline": True},
            ],
            "color": 3066993 if analysis.signal.value == "BUY" else 15158332 if analysis.signal.value == "SELL" else 9807270
        }
        
        await self.notify_all(message, embed)

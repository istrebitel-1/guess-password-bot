import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from src.handlers import register_handlers
from src.settings import get_settings


logger = logging.getLogger(__name__)


class TelegramBot:
    """Task Runner to host telegram bot"""

    def __init__(self):
        self._settings = get_settings()

        self.bot = Bot(token=self._settings.TELEGRAM_BOT_API_TOKEN)
        self.dp = Dispatcher(storage=MemoryStorage())

        self._is_running = True

    async def shutdown(self) -> None:
        """Shutdown runner process"""
        self._is_running = False
        await self.bot.close()

    async def setup_bot(self):
        """Setup Tg Bot"""

        register_handlers(self.dp)
        commands = [
            # BotCommand(command="/start", description="Start the bot"),
            BotCommand(command="/menu", description="Показать меню"),
        ]

        await self.bot.set_my_commands(commands)

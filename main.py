import asyncio
import logging

from dotenv import load_dotenv

from src.bot_runner_task import TelegramBot


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


async def run_bot():
    runner = TelegramBot()
    await runner.setup_bot()
    await runner.dp.start_polling(runner.bot)


if __name__ == "__main__":
    asyncio.run(run_bot())

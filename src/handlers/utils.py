import logging
import random

import aiohttp


logger = logging.getLogger(__name__)


async def get_random_secret_phrase() -> str:
    """Get secret phrase"""

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://random-word-api.herokuapp.com/word"
            ) as response:
                phrase: str = (await response.json())[0]
    except Exception:
        phrases = ["TEST", "WORD", "KEKW"]
        phrase = random.choice(phrases)

    return phrase.upper()

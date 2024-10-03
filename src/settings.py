import logging
from functools import lru_cache
from importlib.metadata import distribution

from pydantic_settings import BaseSettings


logger = logging.getLogger(__name__)
users_dict: dict[str, list[dict]] = {}


class Settings(BaseSettings):
    """App settings"""

    class ConfigDict:
        env_file = ".env"

    APP_VERSION: str

    TELEGRAM_BOT_API_TOKEN: str
    OPEN_AI_API_KEY: str
    OPEN_AI_LLM_MODEL: str = "gpt-4o-2024-08-06"
    OPEN_AI_TIMEOUT: int = 30
    OPEN_AI_RETRIES: int = 3
    OPEN_AI_PROXY_URL: str | None = None

    # fmt: off
    TELEGRAM_MENU_HANDLER_MESSAGE_WELCOME: str = "Выберите действие:"
    TELEGRAM_MENU_HANDLER_MESSAGE_ITEM_PASSWORD_PROTECTION: str = "Вызнать Пароль"

    TELEGRAM_PASSWORD_GAME_HANDLER_MESSAGE_RULES: str = (
        "Твоя задача - получить пароль от бота.\n\nУровень сложности: {level}/1"
    )
    TELEGRAM_PASSWORD_GAME_HANDLER_MESSAGE_RESULT_ALREADY_SENT: str = "Кажется, ты уже отправил результат..."
    TELEGRAM_PASSWORD_GAME_HANDLER_MESSAGE_NO_ATTEMPTS: str = "Кажется, ты уже исчерпал все свои попытки..."
    TELEGRAM_PASSWORD_GAME_HANDLER_MESSAGE_START: str = "Поехали!"
    TELEGRAM_PASSWORD_GAME_HANDLER_MESSAGE_SEND_BUTTON: str = "Ввести пароль"
    TELEGRAM_PASSWORD_GAME_HANDLER_MESSAGE_RETRY: str = "Заново"
    TELEGRAM_PASSWORD_GAME_HANDLER_MESSAGE_BACK_BUTTON: str = "Вернуться в меню"
    TELEGRAM_PASSWORD_GAME_HANDLER_MESSAGE_NEXT_LEVEL: str = "Продолжить"
    TELEGRAM_PASSWORD_GAME_HANDLER_MESSAGE_NO_GAME_AVAILABLE: str = "Пока нет активных игр или ты уже все прошёл..."
    TELEGRAM_PASSWORD_GAME_HANDLER_MESSAGE_LISTENING: str = "Я вас внимательно слушаю"
    TELEGRAM_PASSWORD_GAME_HANDLER_MESSAGE_PASSWORD_CORRECT: str = "Да, пароль верный, уровень пройден!"
    TELEGRAM_PASSWORD_GAME_HANDLER_MESSAGE_PASSWORD_INCORRECT: str = "Пароль неверный"
    TELEGRAM_PASSWORD_GAME_HANDLER_MESSAGE_INPUT_PASSWORD: str = "Введите пароль"
    TELEGRAM_ERROR_OCCURED_MESSAGE: str = "Что-то пошло не по плану..."
    TELEGRAM_START_CALLBACK_MESSAGE_NEW_USER: str = "Привет, начнем?"
    # fmt: on


@lru_cache()
def get_settings() -> Settings:
    return Settings(  # type: ignore
        APP_VERSION=distribution("guess-password-bot").version,
    )

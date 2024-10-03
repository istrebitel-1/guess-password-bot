from aiogram import Dispatcher

from src.handlers.menu_handler import register_menu_handlers
from src.handlers.start_handler import register_start_handlers
from src.handlers.steal_password_game_handler import register_password_game_handlers


__all__ = [
    "register_handlers",
]


def register_handlers(dp: Dispatcher) -> None:
    register_menu_handlers(dp)
    register_start_handlers(dp)
    register_password_game_handlers(dp)

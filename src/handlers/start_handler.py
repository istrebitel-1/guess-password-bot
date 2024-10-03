import logging

from aiogram import Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.settings import get_settings, users_dict


logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("start"))
async def start_command(message: types.Message) -> None:
    """Start handler"""
    if not message.from_user:
        raise ValueError(f"Invalid object received: {message}")

    settings = get_settings()

    if not users_dict.get(str(message.from_user.id)):
        users_dict[str(message.from_user.id)] = []

        logger.info("User `%s` created", message.from_user.id)

    buttons = [
        [
            InlineKeyboardButton(
                text=settings.TELEGRAM_MENU_HANDLER_MESSAGE_ITEM_PASSWORD_PROTECTION,
                callback_data="password_protection",
            ),
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer(
        settings.TELEGRAM_START_CALLBACK_MESSAGE_NEW_USER, reply_markup=keyboard
    )


def register_start_handlers(dp: Dispatcher):
    dp.include_router(router)

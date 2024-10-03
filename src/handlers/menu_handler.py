import logging

from aiogram import Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.settings import get_settings


logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("menu"))
async def main_menu(
    message: types.Message,
    state: FSMContext,
):
    """Main menu handler"""
    if not message.from_user:
        raise ValueError(f"Invalid object received: {message}")

    settings = get_settings()
    await state.clear()

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
        settings.TELEGRAM_MENU_HANDLER_MESSAGE_WELCOME, reply_markup=keyboard
    )


def register_menu_handlers(dp: Dispatcher):
    dp.include_router(router)

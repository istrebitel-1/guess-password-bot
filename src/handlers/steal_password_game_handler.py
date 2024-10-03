import logging

from aiogram import Dispatcher, F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    InaccessibleMessage,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from src.handlers.menu_handler import main_menu
from src.handlers.utils import get_random_secret_phrase
from src.services.openai_serivce import OpenAiLLMService
from src.services.prompts import lvl_1_password_steal_game_prompt
from src.settings import get_settings, users_dict


logger = logging.getLogger(__name__)
router = Router()


class PasswordAttempt(StatesGroup):
    prompt_input = State()
    password_input = State()
    secret_phrase = State()
    message = State()
    level = State()


@router.callback_query(F.data == "password_protection")
async def password_game_rules(
    callback_query: types.CallbackQuery,
    state: FSMContext,
) -> None:
    """Rules handler"""
    if not callback_query.message:
        raise ValueError(f"Invalid object received: {callback_query}")
    if isinstance(callback_query.message, InaccessibleMessage):
        raise ValueError(f"Invalid object received: {callback_query}")

    settings = get_settings()

    if callback_query.message.reply_markup:
        await callback_query.message.delete_reply_markup()

    game_info: list[dict] | None = users_dict.get(str(callback_query.from_user.id))

    if game_info and len(game_info) > 1:
        await callback_query.message.answer(
            settings.TELEGRAM_PASSWORD_GAME_HANDLER_MESSAGE_NO_GAME_AVAILABLE
        )
        return None

    word = await get_random_secret_phrase()
    level = len(game_info or []) + 1

    game = {
        "current_word": word,
        "level": level,
    }
    if not game_info:
        users_dict["str(callback_query.from_user.id)"] = [game]
    else:
        game_info.append(game)

    await state.update_data(
        secret_phrase=word,
        level=level,
    )

    buttons = [
        [
            InlineKeyboardButton(
                text=settings.TELEGRAM_PASSWORD_GAME_HANDLER_MESSAGE_START,
                callback_data="password_protection_start",
            ),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback_query.message.answer(
        settings.TELEGRAM_PASSWORD_GAME_HANDLER_MESSAGE_RULES.format(
            level=level,
        ),
        reply_markup=keyboard,
    )


@router.callback_query(F.data == "password_protection_start")
async def process_password_game(
    callback_query: types.CallbackQuery,
    state: FSMContext,
):
    """Process game handler"""
    if not callback_query.message:
        raise ValueError(f"Invalid object received: {callback_query}")
    if isinstance(callback_query.message, InaccessibleMessage):
        raise ValueError(f"Invalid object received: {callback_query}")

    settings = get_settings()

    logger.info("User %s start password game", callback_query.from_user.id)

    await callback_query.message.edit_reply_markup(reply_markup=None)

    await callback_query.message.answer(
        settings.TELEGRAM_PASSWORD_GAME_HANDLER_MESSAGE_LISTENING
    )
    await state.set_state(PasswordAttempt.prompt_input)


@router.message(PasswordAttempt.prompt_input)
async def handle_prompt_response(
    message: types.Message,
    state: FSMContext,
):
    """Handle response handler"""
    if not message.text:
        raise ValueError(f"Invalid object received: {message}")
    if not message.from_user:
        raise ValueError(f"Invalid object received: {message}")

    data = await state.get_data()
    settings = get_settings()

    if reply_message := data.get("message"):
        await reply_message.edit_reply_markup(reply_markup=None)
        await state.update_data(message=None)

    llm_model = settings.OPEN_AI_LLM_MODEL
    match data["level"]:
        case 1:
            system_prompt = lvl_1_password_steal_game_prompt.format(
                secret_phrase=data["secret_phrase"],
            )
            llm_model = "gpt-3.5-turbo-0125"

    openai_service = OpenAiLLMService(llm_model=llm_model)

    bot_answer = await openai_service.ainvoke(
        system_prompt=system_prompt,
        user_input=message.text,
    )

    buttons = [
        InlineKeyboardButton(
            text=settings.TELEGRAM_PASSWORD_GAME_HANDLER_MESSAGE_SEND_BUTTON,
            callback_data="submit_password_protection",
        ),
        InlineKeyboardButton(
            text=settings.TELEGRAM_PASSWORD_GAME_HANDLER_MESSAGE_BACK_BUTTON,
            callback_data="back_to_menu",
        ),
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])

    message_marked = await message.answer(text=bot_answer, reply_markup=keyboard)
    await state.update_data(message=message_marked)


@router.message(PasswordAttempt.password_input)
async def check_prompt(
    message: types.Message,
    state: FSMContext,
):
    """Check prompt handler"""
    if not message.text:
        raise ValueError(f"Invalid object received: {message}")
    if not message.from_user:
        raise ValueError(f"Invalid object received: {message}")

    data = await state.get_data()
    settings = get_settings()

    logger.info(
        "User %s sent secret phrase, start checks",
        message.from_user.id,
    )

    try:
        # Compare phrase
        if new_detected_flag := data["secret_phrase"].lower() in message.text.lower():
            answer_text = (
                settings.TELEGRAM_PASSWORD_GAME_HANDLER_MESSAGE_PASSWORD_CORRECT
            )

            if data["level"] == 1:
                keyboard = None
            else:
                buttons = [
                    InlineKeyboardButton(
                        text=settings.TELEGRAM_PASSWORD_GAME_HANDLER_MESSAGE_NEXT_LEVEL,
                        callback_data="password_protection",
                    ),
                ]
                keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])

        else:
            answer_text = (
                settings.TELEGRAM_PASSWORD_GAME_HANDLER_MESSAGE_PASSWORD_INCORRECT
            )
            buttons = [
                InlineKeyboardButton(
                    text=settings.TELEGRAM_PASSWORD_GAME_HANDLER_MESSAGE_SEND_BUTTON,
                    callback_data="submit_password_protection",
                ),
                InlineKeyboardButton(
                    text=settings.TELEGRAM_PASSWORD_GAME_HANDLER_MESSAGE_BACK_BUTTON,
                    callback_data="back_to_menu",
                ),
            ]
            keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])

        if new_detected_flag:
            await state.clear()

        await message.answer(answer_text, reply_markup=keyboard)

    except Exception as e:
        logger.error(
            "An error occured while processing prompt for user %s: %s",
            message.from_user.id,
            str(e),
        )
        await message.answer(settings.TELEGRAM_ERROR_OCCURED_MESSAGE)

    logger.info("Finished secret phrase checks for user %s", message.from_user.id)


@router.callback_query(F.data == "submit_password_protection")
async def submit_prompt(
    callback_query: types.CallbackQuery,
    state: FSMContext,
):
    """Submit handler"""
    if not callback_query.message:
        raise ValueError(f"Invalid object received: {callback_query}")
    if isinstance(callback_query.message, InaccessibleMessage):
        raise ValueError(f"Invalid object received: {callback_query}")

    data = await state.get_data()
    settings = get_settings()

    if reply_message := data.get("message"):
        await reply_message.edit_reply_markup(reply_markup=None)
        await state.update_data(message=None)

    await callback_query.message.answer(
        settings.TELEGRAM_PASSWORD_GAME_HANDLER_MESSAGE_INPUT_PASSWORD
    )
    await state.set_state(PasswordAttempt.password_input)


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(
    callback_query: types.CallbackQuery,
    state: FSMContext,
):
    """Back handler"""
    if not callback_query.message:
        raise ValueError(f"Invalid object received: {callback_query}")
    if isinstance(callback_query.message, InaccessibleMessage):
        raise ValueError(f"Invalid object received: {callback_query}")

    await callback_query.message.edit_reply_markup(reply_markup=None)
    await main_menu(callback_query.message, state)


def register_password_game_handlers(dp: Dispatcher):
    dp.include_router(router)

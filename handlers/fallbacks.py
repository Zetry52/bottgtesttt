from aiogram import Router
from aiogram.types import CallbackQuery, Message

from keyboards.inline import main_menu_keyboard
from utils.messages import FALLBACK_TEXT, UNKNOWN_CALLBACK_TEXT

router = Router()


@router.message()
async def fallback_message(message: Message) -> None:
    await message.answer(FALLBACK_TEXT, reply_markup=main_menu_keyboard())


@router.callback_query()
async def fallback_callback(callback: CallbackQuery) -> None:
    await callback.answer(UNKNOWN_CALLBACK_TEXT)

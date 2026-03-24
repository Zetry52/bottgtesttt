import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message

from keyboards.inline import (
    GO_HOME_CALLBACK,
    help_keyboard,
    main_menu_keyboard,
)
from utils.config import settings
from utils.messages import HELP_TEXT, START_CAPTION

router = Router()
logger = logging.getLogger(__name__)


async def send_main_menu(message: Message, state: FSMContext) -> None:
    await state.clear()

    if settings.logo_path.exists():
        photo = FSInputFile(settings.logo_path)
        await message.answer_photo(
            photo=photo,
            caption=START_CAPTION,
            reply_markup=main_menu_keyboard(),
        )
        return

    logger.warning("Logo file not found: %s", settings.logo_path)
    await message.answer(START_CAPTION, reply_markup=main_menu_keyboard())


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext) -> None:
    await send_main_menu(message, state)


@router.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(HELP_TEXT, reply_markup=help_keyboard())


@router.callback_query(F.data == GO_HOME_CALLBACK)
async def go_home(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()

    if callback.message:
        await send_main_menu(callback.message, state)

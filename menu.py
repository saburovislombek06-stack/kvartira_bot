# -*- coding: utf-8 -*-
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import database as db
from states import MainMenu
from locales import t
from keyboards import main_menu_kb
from text_match import any_lang

router = Router(name="menu")


async def show_main_menu(message: Message, state: FSMContext, lang: str):
    await state.set_state(MainMenu.menu)
    await message.answer(t("main_menu", lang), reply_markup=main_menu_kb(lang))


@router.message(F.text.in_(any_lang("btn_main_menu")))
async def go_main_menu(message: Message, state: FSMContext):
    """Har qanday bosqichda bosilsa - barcha amallar bekor, asosiy menyuga qaytish."""
    lang = await db.get_user_language(message.from_user.id)
    await state.clear()
    await show_main_menu(message, state, lang)


@router.message(MainMenu.menu, F.text.in_(any_lang("btn_sell")))
async def menu_sell(message: Message, state: FSMContext):
    from handlers.sell import start_sell
    await start_sell(message, state)


@router.message(MainMenu.menu, F.text.in_(any_lang("btn_buy")))
async def menu_buy(message: Message, state: FSMContext):
    from handlers.buy import start_buy
    await start_buy(message, state)


@router.message(MainMenu.menu, F.text.in_(any_lang("btn_rent_out")))
async def menu_rent_out(message: Message, state: FSMContext):
    from handlers.rent_out import start_rent_out
    await start_rent_out(message, state)


@router.message(MainMenu.menu, F.text.in_(any_lang("btn_rent_in")))
async def menu_rent_in(message: Message, state: FSMContext):
    from handlers.rent_in import start_rent_in
    await start_rent_in(message, state)


@router.message(MainMenu.menu, F.text.in_(any_lang("btn_my_ads")))
async def menu_my_ads(message: Message, state: FSMContext):
    from handlers.my_ads import start_my_ads
    await start_my_ads(message, state)

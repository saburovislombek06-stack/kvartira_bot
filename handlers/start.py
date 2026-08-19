# -*- coding: utf-8 -*-
import re
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import database as db
from states import Registration, MainMenu
from locales import t
from keyboards import language_kb, phone_request_kb, main_menu_kb

router = Router(name="start")

PHONE_RE = re.compile(r"^\+?\d{9,13}$")


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    user = await db.get_user(message.from_user.id)
    if user and user["full_name"] and user["phone"]:
        # Allaqachon ro'yxatdan o'tgan - to'g'ridan-to'g'ri asosiy menyu
        lang = user["language"]
        await state.set_state(MainMenu.menu)
        await message.answer(t("main_menu", lang), reply_markup=main_menu_kb(lang))
        return
    await state.set_state(Registration.choosing_language)
    await message.answer(t("choose_language", "uz"), reply_markup=language_kb())


@router.callback_query(Registration.choosing_language, F.data.startswith("lang:"))
async def choose_language(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.split(":", 1)[1]
    await state.update_data(language=lang)
    await db.upsert_user(callback.from_user.id, language=lang)
    await state.set_state(Registration.entering_fullname)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(t("ask_fullname", lang))
    await callback.answer()


@router.message(Registration.entering_fullname)
async def enter_fullname(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "uz")
    full_name = message.text.strip()
    if len(full_name.split()) < 1 or len(full_name) < 2:
        await message.answer(t("ask_fullname", lang))
        return
    await state.update_data(full_name=full_name)
    await db.upsert_user(message.from_user.id, full_name=full_name)
    await state.set_state(Registration.entering_phone)
    await message.answer(t("ask_phone", lang), reply_markup=phone_request_kb(lang))


@router.message(Registration.entering_phone, F.contact)
async def enter_phone_contact(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    await finish_registration(message, state, phone)


@router.message(Registration.entering_phone, F.text)
async def enter_phone_text(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "uz")
    phone = message.text.strip()
    if not PHONE_RE.match(phone.replace(" ", "")):
        await message.answer(t("ask_phone", lang), reply_markup=phone_request_kb(lang))
        return
    await finish_registration(message, state, phone)


async def finish_registration(message: Message, state: FSMContext, phone: str):
    data = await state.get_data()
    lang = data.get("language", "uz")
    full_name = data.get("full_name", "")
    await db.upsert_user(message.from_user.id, phone=phone)
    await state.set_state(MainMenu.menu)
    await message.answer(t("registration_done", lang, name=full_name))
    await message.answer(t("main_menu", lang), reply_markup=main_menu_kb(lang))

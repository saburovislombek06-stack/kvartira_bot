# -*- coding: utf-8 -*-
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

import database as db
from states import SellHouse
from locales import t
from keyboards import (
    back_main_kb, photo_more_kb, region_kb, district_kb, skip_kb, main_menu_kb,
)
from regions import region_list, region_name, districts_of
from text_match import any_lang

router = Router(name="sell")

MIN_PHOTOS = 2
MAX_PHOTOS = 10


async def start_sell(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    await state.update_data(photos=[])
    await state.set_state(SellHouse.photos)
    await message.answer(
        t("ask_photos_sell", lang, count=0),
        reply_markup=back_main_kb(lang),
    )


@router.message(SellHouse.photos, F.text.in_(any_lang("btn_back")))
async def sell_photos_back(message: Message, state: FSMContext):
    from handlers.menu import show_main_menu
    lang = await db.get_user_language(message.from_user.id)
    await state.clear()
    await show_main_menu(message, state, lang)


@router.message(SellHouse.photos, F.photo)
async def sell_photo_received(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    data = await state.get_data()
    photos = data.get("photos", [])
    photos.append(message.photo[-1].file_id)
    await state.update_data(photos=photos)
    count = len(photos)

    if count >= MAX_PHOTOS:
        await message.answer(t("max_photos_reached", lang))
        await ask_region(message, state, lang)
        return

    if count < MIN_PHOTOS:
        await message.answer(t("ask_photos_sell", lang, count=count), reply_markup=back_main_kb(lang))
        return

    await state.set_state(SellHouse.ask_more_photo)
    await message.answer(
        t("photo_added_ask_more", lang, count=count),
        reply_markup=photo_more_kb(lang, can_add_more=True),
    )


@router.message(SellHouse.photos, ~F.photo, ~F.text.in_(any_lang("btn_main_menu")))
async def sell_photo_invalid(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    data = await state.get_data()
    count = len(data.get("photos", []))
    await message.answer(t("min_photos_not_reached", lang, min=MIN_PHOTOS) if count < MIN_PHOTOS
                          else t("ask_photos_sell", lang, count=count),
                          reply_markup=back_main_kb(lang))


@router.message(SellHouse.ask_more_photo, F.text.in_(any_lang("btn_yes_more_photo")))
async def sell_more_photo_yes(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    data = await state.get_data()
    count = len(data.get("photos", []))
    await state.set_state(SellHouse.photos)
    await message.answer(t("ask_photos_sell", lang, count=count), reply_markup=back_main_kb(lang))


@router.message(SellHouse.ask_more_photo, F.text.in_(any_lang("btn_no_finish_photo")))
async def sell_more_photo_no(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    await ask_region(message, state, lang)


@router.message(SellHouse.ask_more_photo, F.text.in_(any_lang("btn_back")))
async def sell_ask_more_back(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    data = await state.get_data()
    photos = data.get("photos", [])
    if photos:
        photos.pop()
        await state.update_data(photos=photos)
    await state.set_state(SellHouse.photos)
    await message.answer(t("ask_photos_sell", lang, count=len(photos)), reply_markup=back_main_kb(lang))


async def ask_region(message: Message, state: FSMContext, lang: str):
    await state.set_state(SellHouse.region)
    await message.answer(t("ask_region", lang), reply_markup=ReplyKeyboardRemove())
    await message.answer(t("ask_region", lang), reply_markup=region_kb(lang))


@router.callback_query(SellHouse.region, F.data.startswith("region:"))
async def sell_region_chosen(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_user_language(callback.from_user.id)
    region_key = callback.data.split(":", 1)[1]
    await state.update_data(region_key=region_key, region_name=region_name(region_key, lang))
    await state.set_state(SellHouse.district)
    await callback.message.edit_text(t("ask_district", lang), reply_markup=district_kb(lang, region_key))
    await callback.answer()


@router.callback_query(SellHouse.region, F.data == "nav:back")
async def sell_region_back(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_user_language(callback.from_user.id)
    await state.set_state(SellHouse.ask_more_photo)
    await callback.message.delete()
    data = await state.get_data()
    count = len(data.get("photos", []))
    await callback.message.answer(t("photo_added_ask_more", lang, count=count), reply_markup=photo_more_kb(lang, True))
    await callback.answer()


@router.callback_query(SellHouse.district, F.data.startswith("district:"))
async def sell_district_chosen(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_user_language(callback.from_user.id)
    data = await state.get_data()
    idx = int(callback.data.split(":", 1)[1])
    district_name = districts_of(data["region_key"])[idx]
    await state.update_data(district=district_name)
    await state.set_state(SellHouse.price)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(t("ask_price_sell", lang), reply_markup=back_main_kb(lang))
    await callback.answer()


@router.callback_query(SellHouse.district, F.data == "nav:back")
async def sell_district_back(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_user_language(callback.from_user.id)
    await state.set_state(SellHouse.region)
    await callback.message.edit_text(t("ask_region", lang), reply_markup=region_kb(lang))
    await callback.answer()


@router.message(SellHouse.price, F.text.in_(any_lang("btn_back")))
async def sell_price_back(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    data = await state.get_data()
    await state.set_state(SellHouse.district)
    await message.answer(t("ask_district", lang), reply_markup=district_kb(lang, data["region_key"]))


@router.message(SellHouse.price, F.text)
async def sell_price_entered(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    await state.update_data(price=message.text.strip())
    await state.set_state(SellHouse.extra_info)
    await message.answer(t("ask_extra_info_optional", lang), reply_markup=skip_kb(lang))


@router.message(SellHouse.extra_info, F.text.in_(any_lang("btn_back")))
async def sell_extra_back(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    await state.set_state(SellHouse.price)
    await message.answer(t("ask_price_sell", lang), reply_markup=back_main_kb(lang))


@router.message(SellHouse.extra_info, F.text.in_(any_lang("btn_skip")))
async def sell_extra_skip(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    await state.update_data(extra_info=None)
    await state.set_state(SellHouse.phone)
    await message.answer(t("ask_contact_phone", lang), reply_markup=back_main_kb(lang))


@router.message(SellHouse.extra_info, F.text)
async def sell_extra_entered(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    await state.update_data(extra_info=message.text.strip())
    await state.set_state(SellHouse.phone)
    await message.answer(t("ask_contact_phone", lang), reply_markup=back_main_kb(lang))


@router.message(SellHouse.phone, F.text.in_(any_lang("btn_back")))
async def sell_phone_back(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    await state.set_state(SellHouse.extra_info)
    await message.answer(t("ask_extra_info_optional", lang), reply_markup=skip_kb(lang))


@router.message(SellHouse.phone, F.text)
async def sell_phone_entered(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    data = await state.get_data()
    listing_id = await db.create_listing(
        user_id=message.from_user.id,
        ad_type="sell",
        region=data["region_name"],
        district=data["district"],
        price=data["price"],
        extra_info=data.get("extra_info"),
        contact_phone=message.text.strip(),
        photos=data.get("photos", []),
    )
    from handlers.menu import show_main_menu
    await state.clear()
    await message.answer(t("ad_published", lang))
    await show_main_menu(message, state, lang)

# -*- coding: utf-8 -*-
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

import database as db
from states import RentOutHouse
from locales import t
from keyboards import back_main_kb, region_kb, district_kb, skip_kb, location_optional_kb
from regions import region_name, districts_of
from text_match import any_lang

router = Router(name="rent_out")

REQUIRED_PHOTOS = 4


async def start_rent_out(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    await state.update_data(photos=[])
    await state.set_state(RentOutHouse.photos)
    await message.answer(t("ask_photos_rent_out", lang, count=0), reply_markup=back_main_kb(lang))


@router.message(RentOutHouse.photos, F.text.in_(any_lang("btn_back")))
async def rent_out_photos_back(message: Message, state: FSMContext):
    from handlers.menu import show_main_menu
    lang = await db.get_user_language(message.from_user.id)
    await state.clear()
    await show_main_menu(message, state, lang)


@router.message(RentOutHouse.photos, F.photo)
async def rent_out_photo_received(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    data = await state.get_data()
    photos = data.get("photos", [])
    photos.append(message.photo[-1].file_id)
    await state.update_data(photos=photos)
    count = len(photos)

    if count >= REQUIRED_PHOTOS:
        await state.set_state(RentOutHouse.price)
        await message.answer(t("ask_price_rent", lang), reply_markup=back_main_kb(lang))
        return

    await message.answer(t("ask_photos_rent_out", lang, count=count), reply_markup=back_main_kb(lang))


@router.message(RentOutHouse.photos, ~F.photo, ~F.text.in_(any_lang("btn_main_menu")))
async def rent_out_photo_invalid(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    data = await state.get_data()
    count = len(data.get("photos", []))
    await message.answer(t("ask_photos_rent_out", lang, count=count), reply_markup=back_main_kb(lang))


@router.message(RentOutHouse.price, F.text.in_(any_lang("btn_back")))
async def rent_out_price_back(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    data = await state.get_data()
    photos = data.get("photos", [])
    if photos:
        photos.pop()
        await state.update_data(photos=photos)
    await state.set_state(RentOutHouse.photos)
    await message.answer(t("ask_photos_rent_out", lang, count=len(photos)), reply_markup=back_main_kb(lang))


@router.message(RentOutHouse.price, F.text)
async def rent_out_price_entered(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    await state.update_data(price=message.text.strip())
    await state.set_state(RentOutHouse.region)
    await message.answer(t("ask_region", lang), reply_markup=ReplyKeyboardRemove())
    await message.answer(t("ask_region", lang), reply_markup=region_kb(lang))


@router.callback_query(RentOutHouse.region, F.data.startswith("region:"))
async def rent_out_region_chosen(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_user_language(callback.from_user.id)
    region_key = callback.data.split(":", 1)[1]
    await state.update_data(region_key=region_key, region_name=region_name(region_key, lang))
    await state.set_state(RentOutHouse.district)
    await callback.message.edit_text(t("ask_district", lang), reply_markup=district_kb(lang, region_key))
    await callback.answer()


@router.callback_query(RentOutHouse.region, F.data == "nav:back")
async def rent_out_region_back(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_user_language(callback.from_user.id)
    await state.set_state(RentOutHouse.price)
    await callback.message.delete()
    await callback.message.answer(t("ask_price_rent", lang), reply_markup=back_main_kb(lang))
    await callback.answer()


@router.callback_query(RentOutHouse.district, F.data.startswith("district:"))
async def rent_out_district_chosen(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_user_language(callback.from_user.id)
    data = await state.get_data()
    idx = int(callback.data.split(":", 1)[1])
    district_name = districts_of(data["region_key"])[idx]
    await state.update_data(district=district_name)
    await state.set_state(RentOutHouse.location)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(t("ask_location", lang), reply_markup=location_optional_kb(lang))
    await callback.answer()


@router.callback_query(RentOutHouse.district, F.data == "nav:back")
async def rent_out_district_back(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_user_language(callback.from_user.id)
    await state.set_state(RentOutHouse.region)
    await callback.message.edit_text(t("ask_region", lang), reply_markup=region_kb(lang))
    await callback.answer()


@router.message(RentOutHouse.location, F.location)
async def rent_out_location_received(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    await state.update_data(lat=message.location.latitude, lon=message.location.longitude)
    await state.set_state(RentOutHouse.extra_info)
    await message.answer(t("ask_rent_terms", lang), reply_markup=skip_kb(lang))


@router.message(RentOutHouse.location, F.text.in_(any_lang("btn_skip")))
async def rent_out_location_skip(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    await state.update_data(lat=None, lon=None)
    await state.set_state(RentOutHouse.extra_info)
    await message.answer(t("ask_rent_terms", lang), reply_markup=skip_kb(lang))


@router.message(RentOutHouse.location, F.text.in_(any_lang("btn_back")))
async def rent_out_location_back(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    data = await state.get_data()
    await state.set_state(RentOutHouse.district)
    await message.answer(t("ask_district", lang), reply_markup=district_kb(lang, data["region_key"]))


@router.message(RentOutHouse.extra_info, F.text.in_(any_lang("btn_back")))
async def rent_out_extra_back(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    await state.set_state(RentOutHouse.location)
    await message.answer(t("ask_location", lang), reply_markup=location_optional_kb(lang))


@router.message(RentOutHouse.extra_info, F.text.in_(any_lang("btn_skip")))
async def rent_out_extra_skip(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    await state.update_data(extra_info=None)
    await state.set_state(RentOutHouse.phone)
    await message.answer(t("ask_contact_phone", lang), reply_markup=back_main_kb(lang))


@router.message(RentOutHouse.extra_info, F.text)
async def rent_out_extra_entered(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    await state.update_data(extra_info=message.text.strip())
    await state.set_state(RentOutHouse.phone)
    await message.answer(t("ask_contact_phone", lang), reply_markup=back_main_kb(lang))


@router.message(RentOutHouse.phone, F.text.in_(any_lang("btn_back")))
async def rent_out_phone_back(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    await state.set_state(RentOutHouse.extra_info)
    await message.answer(t("ask_rent_terms", lang), reply_markup=skip_kb(lang))


@router.message(RentOutHouse.phone, F.text)
async def rent_out_phone_entered(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    data = await state.get_data()
    await db.create_listing(
        user_id=message.from_user.id,
        ad_type="rent_out",
        region=data["region_name"],
        district=data["district"],
        price=data["price"],
        extra_info=None,
        contact_phone=message.text.strip(),
        photos=data.get("photos", []),
        rent_terms=data.get("extra_info"),
        lat=data.get("lat"),
        lon=data.get("lon"),
    )
    from handlers.menu import show_main_menu
    await state.clear()
    await message.answer(t("ad_published", lang))
    await show_main_menu(message, state, lang)

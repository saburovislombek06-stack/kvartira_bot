# -*- coding: utf-8 -*-
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

import database as db
from states import RentInHouse
from locales import t
from keyboards import region_kb, district_kb, ad_extra_kb, location_kb
from regions import region_name, districts_of
from text_match import any_lang
from utils import haversine_km
from config import NEARBY_RADIUS_KM
from handlers.buy import send_one_listing

router = Router(name="rent_in")


async def start_rent_in(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    await state.set_state(RentInHouse.region)
    await message.answer(t("ask_region", lang), reply_markup=ReplyKeyboardRemove())
    await message.answer(t("ask_region", lang), reply_markup=region_kb(lang))


@router.callback_query(RentInHouse.region, F.data.startswith("region:"))
async def rent_in_region_chosen(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_user_language(callback.from_user.id)
    region_key = callback.data.split(":", 1)[1]
    await state.update_data(region_key=region_key, region_name=region_name(region_key, lang))
    await state.set_state(RentInHouse.district)
    await callback.message.edit_text(t("ask_district", lang), reply_markup=district_kb(lang, region_key))
    await callback.answer()


@router.callback_query(RentInHouse.region, F.data == "nav:back")
async def rent_in_region_back(callback: CallbackQuery, state: FSMContext):
    from handlers.menu import show_main_menu
    lang = await db.get_user_language(callback.from_user.id)
    await state.clear()
    await callback.message.delete()
    await show_main_menu(callback.message, state, lang)
    await callback.answer()


@router.callback_query(RentInHouse.district, F.data.startswith("district:"))
async def rent_in_district_chosen(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_user_language(callback.from_user.id)
    data = await state.get_data()
    idx = int(callback.data.split(":", 1)[1])
    district_name = districts_of(data["region_key"])[idx]
    await callback.message.edit_reply_markup(reply_markup=None)

    listings = await db.get_listings("rent_out", data["region_name"], district_name)
    if not listings:
        await callback.message.answer(t("no_ads_found", lang))
    else:
        await callback.message.answer(t("ads_found", lang, count=len(listings)))
        for listing in listings:
            await send_one_listing(callback.message, lang, listing)

    await state.set_state(RentInHouse.browsing)
    await callback.message.answer(t("ask_location", lang), reply_markup=ad_extra_kb(lang))
    await callback.answer()


@router.callback_query(RentInHouse.district, F.data == "nav:back")
async def rent_in_district_back(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_user_language(callback.from_user.id)
    await state.set_state(RentInHouse.region)
    await callback.message.edit_text(t("ask_region", lang), reply_markup=region_kb(lang))
    await callback.answer()


@router.callback_query(RentInHouse.browsing, F.data == "use_location")
async def rent_in_use_location(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_user_language(callback.from_user.id)
    await state.set_state(RentInHouse.waiting_location)
    await callback.message.answer(t("ask_location", lang), reply_markup=location_kb(lang))
    await callback.answer()


@router.message(RentInHouse.waiting_location, F.location)
async def rent_in_location_received(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    lat, lon = message.location.latitude, message.location.longitude
    all_rent_out = await db.get_all_active_by_type("rent_out")
    nearby = [
        listing for listing in all_rent_out
        if haversine_km(lat, lon, listing["lat"], listing["lon"]) <= NEARBY_RADIUS_KM
    ]
    if not nearby:
        await message.answer(t("no_ads_found", lang))
    else:
        await message.answer(t("ads_found", lang, count=len(nearby)))
        for listing in nearby:
            await send_one_listing(message, lang, listing)

    from handlers.menu import show_main_menu
    await state.clear()
    await show_main_menu(message, state, lang)


@router.message(RentInHouse.waiting_location, F.text.in_(any_lang("btn_back")))
async def rent_in_location_back(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    await state.set_state(RentInHouse.browsing)
    await message.answer(t("ask_location", lang), reply_markup=ad_extra_kb(lang))

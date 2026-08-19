# -*- coding: utf-8 -*-
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

import database as db
from states import BuyHouse
from locales import t
from keyboards import region_kb, district_kb, back_main_kb
from regions import region_name, districts_of
from text_match import any_lang

router = Router(name="buy")


async def start_buy(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    await state.set_state(BuyHouse.region)
    await message.answer(t("choose_region_search", lang), reply_markup=ReplyKeyboardRemove())
    await message.answer(t("ask_region", lang), reply_markup=region_kb(lang))


@router.callback_query(BuyHouse.region, F.data.startswith("region:"))
async def buy_region_chosen(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_user_language(callback.from_user.id)
    region_key = callback.data.split(":", 1)[1]
    await state.update_data(region_key=region_key, region_name=region_name(region_key, lang))
    await state.set_state(BuyHouse.district)
    await callback.message.edit_text(t("ask_district", lang), reply_markup=district_kb(lang, region_key))
    await callback.answer()


@router.callback_query(BuyHouse.region, F.data == "nav:back")
async def buy_region_back(callback: CallbackQuery, state: FSMContext):
    from handlers.menu import show_main_menu
    lang = await db.get_user_language(callback.from_user.id)
    await state.clear()
    await callback.message.delete()
    await show_main_menu(callback.message, state, lang)
    await callback.answer()


@router.callback_query(BuyHouse.district, F.data.startswith("district:"))
async def buy_district_chosen(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_user_language(callback.from_user.id)
    data = await state.get_data()
    idx = int(callback.data.split(":", 1)[1])
    district_name = districts_of(data["region_key"])[idx]
    await callback.message.edit_reply_markup(reply_markup=None)
    await send_listings(callback.message, lang, data["region_name"], district_name)
    from handlers.menu import show_main_menu
    await show_main_menu(callback.message, state, lang)
    await callback.answer()


@router.callback_query(BuyHouse.district, F.data == "nav:back")
async def buy_district_back(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_user_language(callback.from_user.id)
    await state.set_state(BuyHouse.region)
    await callback.message.edit_text(t("ask_region", lang), reply_markup=region_kb(lang))
    await callback.answer()


async def send_listings(message: Message, lang: str, region: str, district: str):
    listings = await db.get_listings("sell", region, district)
    if not listings:
        await message.answer(t("no_ads_found", lang))
        return
    await message.answer(t("ads_found", lang, count=len(listings)))
    for listing in listings:
        await send_one_listing(message, lang, listing)


async def send_one_listing(message: Message, lang: str, listing):
    seller = await db.get_user(listing["user_id"])
    seller_name = seller["full_name"] if seller else "-"
    photos = await db.get_listing_photos(listing["id"])
    caption = (
        f"🏠 {listing['region']}, {listing['district']}\n"
        f"💰 {listing['price']} so'm\n"
        + (f"📝 {listing['extra_info']}\n" if listing["extra_info"] else "")
        + t("contact_seller", lang, phone=listing["contact_phone"], name=seller_name)
    )
    if photos:
        if len(photos) == 1:
            await message.answer_photo(photos[0], caption=caption)
        else:
            media = [InputMediaPhoto(media=p) for p in photos[:10]]
            media[0].caption = caption
            await message.answer_media_group(media)
    else:
        await message.answer(caption)

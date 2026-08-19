# -*- coding: utf-8 -*-
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext

import database as db
from locales import t
from keyboards import listing_contact_kb

router = Router(name="my_ads")


async def start_my_ads(message: Message, state: FSMContext):
    lang = await db.get_user_language(message.from_user.id)
    listings = await db.get_user_listings(message.from_user.id)
    if not listings:
        await message.answer(t("my_ads_empty", lang))
        return
    await message.answer(t("my_ads_title", lang))
    for listing in listings:
        await send_own_listing(message, lang, listing)


async def send_own_listing(message: Message, lang: str, listing):
    photos = await db.get_listing_photos(listing["id"])
    type_label = "🏷 Sotish" if listing["ad_type"] == "sell" else "🔑 Ijaraga berish"
    caption = (
        f"{type_label}\n"
        f"🏠 {listing['region']}, {listing['district']}\n"
        f"💰 {listing['price']} so'm"
    )
    kb = listing_contact_kb(lang, listing["id"], is_owner=True)
    if photos:
        await message.answer_photo(photos[0], caption=caption, reply_markup=kb)
    else:
        await message.answer(caption, reply_markup=kb)


@router.callback_query(F.data.startswith("remove:"))
async def remove_listing(callback: CallbackQuery, state: FSMContext):
    lang = await db.get_user_language(callback.from_user.id)
    listing_id = int(callback.data.split(":", 1)[1])
    ok = await db.deactivate_listing(listing_id, callback.from_user.id)
    if ok:
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer(t("ad_removed", lang), show_alert=True)
    else:
        await callback.answer()

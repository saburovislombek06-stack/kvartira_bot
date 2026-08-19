# -*- coding: utf-8 -*-
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,
)
from regions import REGIONS, region_list, region_name, districts_of
from locales import t, LANG_NAMES


def language_kb() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=LANG_NAMES["uz"], callback_data="lang:uz")],
        [InlineKeyboardButton(text=LANG_NAMES["ru"], callback_data="lang:ru")],
        [InlineKeyboardButton(text=LANG_NAMES["kk"], callback_data="lang:kk")],
        [InlineKeyboardButton(text=LANG_NAMES["kaa"], callback_data="lang:kaa")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def phone_request_kb(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t("share_phone_btn", lang), request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def main_menu_kb(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t("btn_sell", lang)), KeyboardButton(text=t("btn_buy", lang))],
            [KeyboardButton(text=t("btn_rent_out", lang)), KeyboardButton(text=t("btn_rent_in", lang))],
            [KeyboardButton(text=t("btn_my_ads", lang))],
        ],
        resize_keyboard=True,
    )


def back_main_kb(lang: str) -> ReplyKeyboardMarkup:
    """Har bir bosqichda ko'rinadigan 'Orqaga' va 'Asosiy menyu' tugmalari."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t("btn_back", lang)), KeyboardButton(text=t("btn_main_menu", lang))]],
        resize_keyboard=True,
    )


def photo_more_kb(lang: str, can_add_more: bool) -> ReplyKeyboardMarkup:
    rows = []
    if can_add_more:
        rows.append([KeyboardButton(text=t("btn_yes_more_photo", lang))])
    rows.append([KeyboardButton(text=t("btn_no_finish_photo", lang))])
    rows.append([KeyboardButton(text=t("btn_back", lang)), KeyboardButton(text=t("btn_main_menu", lang))])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def skip_kb(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t("btn_skip", lang))],
            [KeyboardButton(text=t("btn_back", lang)), KeyboardButton(text=t("btn_main_menu", lang))],
        ],
        resize_keyboard=True,
    )


def region_kb(lang: str) -> InlineKeyboardMarkup:
    rows = []
    row = []
    for key in region_list():
        row.append(InlineKeyboardButton(text=region_name(key, lang), callback_data=f"region:{key}"))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([InlineKeyboardButton(text=t("btn_back", lang), callback_data="nav:back")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def district_kb(lang: str, region_key: str) -> InlineKeyboardMarkup:
    rows = []
    row = []
    for i, dist in enumerate(districts_of(region_key)):
        row.append(InlineKeyboardButton(text=dist, callback_data=f"district:{i}"))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([InlineKeyboardButton(text=t("btn_back", lang), callback_data="nav:back")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def location_kb(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t("btn_send_location", lang), request_location=True)],
            [KeyboardButton(text=t("btn_back", lang)), KeyboardButton(text=t("btn_main_menu", lang))],
        ],
        resize_keyboard=True,
    )


def location_optional_kb(lang: str) -> ReplyKeyboardMarkup:
    """Ijaraga beruvchi uchun ixtiyoriy lokatsiya (yaqin-atrofdan qidiruv ishlashi uchun)."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t("btn_send_location", lang), request_location=True)],
            [KeyboardButton(text=t("btn_skip", lang))],
            [KeyboardButton(text=t("btn_back", lang)), KeyboardButton(text=t("btn_main_menu", lang))],
        ],
        resize_keyboard=True,
    )


def ad_extra_kb(lang: str) -> InlineKeyboardMarkup:
    """Sotib olish/ijaraga olish natijalari ostida location bo'yicha qidirish tugmasi."""
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=t("btn_extra_location", lang), callback_data="use_location")]]
    )


def listing_contact_kb(lang: str, listing_id: int, is_owner: bool = False) -> InlineKeyboardMarkup:
    if is_owner:
        return InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=t("btn_remove_ad", lang), callback_data=f"remove:{listing_id}")]]
        )
    return InlineKeyboardMarkup(inline_keyboard=[])

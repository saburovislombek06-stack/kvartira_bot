# -*- coding: utf-8 -*-
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

import database as db
from config import ADMIN_IDS
from locales import t

router = Router(name="admin")


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    if not is_admin(message.from_user.id):
        lang = await db.get_user_language(message.from_user.id)
        await message.answer(t("admin_not_authorized", lang))
        return
    s = await db.stats_summary()
    text = (
        "📊 <b>Statistika</b>\n\n"
        f"👥 Ro'yxatdan o'tgan foydalanuvchilar: <b>{s['users_count']}</b>\n"
        f"📋 Faol e'lonlar: <b>{s['active_listings']}</b>\n"
        f"🗂 Jami e'lonlar (o'chirilganlari bilan): <b>{s['total_listings']}</b>\n\n"
        "Turlari bo'yicha (faol):\n"
        f"  🏷 Sotish: {s['by_type'].get('sell', 0)}\n"
        f"  🔑 Ijaraga berish: {s['by_type'].get('rent_out', 0)}\n"
    )
    await message.answer(text, parse_mode="HTML")


@router.message(Command("users"))
async def cmd_users(message: Message):
    if not is_admin(message.from_user.id):
        lang = await db.get_user_language(message.from_user.id)
        await message.answer(t("admin_not_authorized", lang))
        return
    users = await db.list_users(limit=50)
    if not users:
        await message.answer("Hozircha foydalanuvchilar yo'q.")
        return
    lines = ["👥 <b>So'nggi foydalanuvchilar</b>:\n"]
    for u in users:
        lines.append(
            f"• {u['full_name'] or '-'} | {u['phone'] or '-'} | id: <code>{u['user_id']}</code> | {u['language']}"
        )
    await message.answer("\n".join(lines), parse_mode="HTML")


@router.message(Command("listings"))
async def cmd_listings(message: Message):
    if not is_admin(message.from_user.id):
        lang = await db.get_user_language(message.from_user.id)
        await message.answer(t("admin_not_authorized", lang))
        return
    listings = await db.list_recent_listings(limit=50)
    if not listings:
        await message.answer("Hozircha e'lonlar yo'q.")
        return
    lines = ["🗂 <b>So'nggi e'lonlar</b>:\n"]
    for l in listings:
        status = "✅ faol" if l["is_active"] else "❌ o'chirilgan"
        type_label = "Sotish" if l["ad_type"] == "sell" else "Ijaraga berish"
        lines.append(
            f"#{l['id']} | {type_label} | {l['region']}, {l['district']} | "
            f"{l['price']} | user:{l['user_id']} | {status}"
        )
    await message.answer("\n".join(lines), parse_mode="HTML")

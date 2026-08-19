# -*- coding: utf-8 -*-
"""
SQLite ustida yupqa async qatlam (aiosqlite).
Jadvallar:
  users     - ro'yxatdan o'tgan foydalanuvchilar
  listings  - e'lonlar (sotish / ijaraga berish), type ustuni bilan ajratiladi
  photos    - e'lonlarga tegishli rasmlar (telegram file_id)
"""
import json
import time
import aiosqlite

DB_PATH = "uy_bot.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    full_name TEXT,
    phone TEXT,
    language TEXT DEFAULT 'uz',
    created_at INTEGER
);

CREATE TABLE IF NOT EXISTS listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    ad_type TEXT NOT NULL,          -- 'sell' | 'rent_out'
    region TEXT,
    district TEXT,
    price TEXT,
    extra_info TEXT,
    contact_phone TEXT,
    rent_terms TEXT,
    lat REAL,
    lon REAL,
    is_active INTEGER DEFAULT 1,
    created_at INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id INTEGER NOT NULL,
    file_id TEXT NOT NULL,
    FOREIGN KEY(listing_id) REFERENCES listings(id)
);
"""


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript(SCHEMA)
        await db.commit()


# ---------- users ----------

async def upsert_user(user_id: int, full_name: str = None, phone: str = None, language: str = None):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
        row = await cur.fetchone()
        if row is None:
            await db.execute(
                "INSERT INTO users (user_id, full_name, phone, language, created_at) VALUES (?,?,?,?,?)",
                (user_id, full_name, phone, language or "uz", int(time.time())),
            )
        else:
            if full_name is not None:
                await db.execute("UPDATE users SET full_name=? WHERE user_id=?", (full_name, user_id))
            if phone is not None:
                await db.execute("UPDATE users SET phone=? WHERE user_id=?", (phone, user_id))
            if language is not None:
                await db.execute("UPDATE users SET language=? WHERE user_id=?", (language, user_id))
        await db.commit()


async def get_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        return await cur.fetchone()


async def get_user_language(user_id: int) -> str:
    user = await get_user(user_id)
    return user["language"] if user else "uz"


# ---------- listings ----------

async def create_listing(user_id: int, ad_type: str, region: str, district: str,
                          price: str, extra_info: str, contact_phone: str,
                          photos: list, rent_terms: str = None,
                          lat: float = None, lon: float = None) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            """INSERT INTO listings
               (user_id, ad_type, region, district, price, extra_info,
                contact_phone, rent_terms, lat, lon, is_active, created_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,1,?)""",
            (user_id, ad_type, region, district, price, extra_info,
             contact_phone, rent_terms, lat, lon, int(time.time())),
        )
        listing_id = cur.lastrowid
        for file_id in photos:
            await db.execute(
                "INSERT INTO photos (listing_id, file_id) VALUES (?,?)",
                (listing_id, file_id),
            )
        await db.commit()
        return listing_id


async def get_listings(ad_type: str, region: str, district: str = None, active_only: bool = True):
    query = "SELECT * FROM listings WHERE ad_type=? AND region=?"
    params = [ad_type, region]
    if district:
        query += " AND district=?"
        params.append(district)
    if active_only:
        query += " AND is_active=1"
    query += " ORDER BY created_at DESC"
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(query, params)
        return await cur.fetchall()


async def get_all_active_by_type(ad_type: str):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM listings WHERE ad_type=? AND is_active=1 AND lat IS NOT NULL",
            (ad_type,),
        )
        return await cur.fetchall()


async def get_listing_photos(listing_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT file_id FROM photos WHERE listing_id=?", (listing_id,))
        rows = await cur.fetchall()
        return [r[0] for r in rows]


async def get_user_listings(user_id: int, active_only: bool = True):
    query = "SELECT * FROM listings WHERE user_id=?"
    params = [user_id]
    if active_only:
        query += " AND is_active=1"
    query += " ORDER BY created_at DESC"
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(query, params)
        return await cur.fetchall()


async def deactivate_listing(listing_id: int, user_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "UPDATE listings SET is_active=0 WHERE id=? AND user_id=?", (listing_id, user_id)
        )
        await db.commit()
        return cur.rowcount > 0


async def get_listing(listing_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM listings WHERE id=?", (listing_id,))
        return await cur.fetchone()


# ---------- admin / stats ----------

async def stats_summary():
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT COUNT(*) FROM users")
        users_count = (await cur.fetchone())[0]

        cur = await db.execute("SELECT COUNT(*) FROM listings WHERE is_active=1")
        active_listings = (await cur.fetchone())[0]

        cur = await db.execute("SELECT COUNT(*) FROM listings")
        total_listings = (await cur.fetchone())[0]

        cur = await db.execute(
            "SELECT ad_type, COUNT(*) FROM listings WHERE is_active=1 GROUP BY ad_type"
        )
        by_type = dict(await cur.fetchall())

        return {
            "users_count": users_count,
            "active_listings": active_listings,
            "total_listings": total_listings,
            "by_type": by_type,
        }


async def list_users(limit: int = 50):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM users ORDER BY created_at DESC LIMIT ?", (limit,)
        )
        return await cur.fetchall()


async def list_recent_listings(limit: int = 50):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM listings ORDER BY created_at DESC LIMIT ?", (limit,)
        )
        return await cur.fetchall()

# 🏠 Uy-joy e'lonlari Telegram boti

Spetsifikatsiyada tasvirlangan barcha funksiyalarni bajaruvchi Telegram bot: uy sotish,
sotib olish, ijaraga berish, ijaraga olish, ko'p tillilik (o'zbek/rus/qozoq/qoraqalpoq)
va admin statistikasi.

## ✅ Amalga oshirilgan funksiyalar

- **Ro'yxatdan o'tish**: til tanlash (4 til) → ism-familiya → telefon raqam (tugma yoki qo'lda)
- **Asosiy menyu**: 5 bo'lim (sotish, sotib olish, ijaraga berish, ijaraga olish, mening reklamalarim)
  + har bir qadamda "⬅️ Orqaga" (1 qadam orqaga) va "🏠 Asosiy menyu" (hammasini bekor qilish) tugmalari
- **Uy sotish**: 2–10 ta rasm (2 tadan keyin avtomatik "yana qo'shasizmi?" so'raladi, 10 tada avtomatik to'xtaydi),
  viloyat → tuman/shahar, narx, ixtiyoriy qo'shimcha ma'lumot, majburiy telefon
- **Uy sotib olish**: viloyat → tuman tanlab, o'sha hududdagi barcha faol e'lonlarni ko'rish (rasm + narx + sotuvchi kontaktlari bilan)
- **Uy ijaraga berish**: aynan 4 ta rasm (majburiy), narx, manzil, ixtiyoriy lokatsiya (yaqin-atrofdan
  qidiruv ishlashi uchun), shartnoma sharoitlari, telefon
- **Uy ijaraga olish**: viloyat/tuman bo'yicha qidiruv **yoki** lokatsiya yuborib 10 km radiusdagi
  barcha e'lonlarni ko'rish
- **Mening reklamalarim**: faol e'lonlaringizni ko'rish va "sotildi/berildi" bo'lsa o'chirish
  (o'chirilgan e'lon boshqa hech kimga ko'rinmaydi)
- **Admin panel** (buyruqlar orqali, faqat `.env` dagi `ADMIN_IDS` ro'yxatidagilar uchun):
  - `/stats` — foydalanuvchilar soni, faol/jami e'lonlar, turlari bo'yicha taqsimot
  - `/users` — so'nggi ro'yxatdan o'tgan foydalanuvchilar ro'yxati
  - `/listings` — so'nggi joylashtirilgan e'lonlar ro'yxati (kim, qachon, holati)
- 12 ta viloyat + Toshkent shahri + Qoraqalpog'iston Respublikasi va ularning barcha
  tuman/shaharlari (`regions.py`) — kerak bo'lsa osongina to'ldirish/tuzatish mumkin

## 📁 Loyiha tuzilishi

```
uy_bot/
├── main.py              # botni ishga tushirish
├── config.py             # BOT_TOKEN, ADMIN_IDS (.env dan)
├── database.py           # SQLite (aiosqlite) - users, listings, photos
├── regions.py             # viloyat/tuman ma'lumotlari (4 tilda nom)
├── locales.py             # interfeys matnlari (uz/ru/kk/kaa)
├── states.py               # FSM holatlar (har bir bosqich)
├── keyboards.py            # klaviaturalar
├── text_match.py            # ko'p tildagi tugma matnini aniqlash
├── utils.py                  # masofa hisoblash (lokatsiya qidiruvi uchun)
├── handlers/
│   ├── start.py               # ro'yxatdan o'tish
│   ├── menu.py                 # asosiy menyu
│   ├── sell.py                  # uy sotish
│   ├── buy.py                    # uy sotib olish
│   ├── rent_out.py                # uy ijaraga berish
│   ├── rent_in.py                  # uy ijaraga olish
│   ├── my_ads.py                    # mening reklamalarim
│   └── admin.py                      # admin statistikasi
├── requirements.txt
└── .env.example
```

## 🚀 Ishga tushirish

1. **Bot yaratish**: Telegram’da [@BotFather](https://t.me/BotFather) ga `/newbot` yuboring, tokenni oling.
2. **O'z Telegram ID ingizni bilish** (admin bo'lish uchun): [@userinfobot](https://t.me/userinfobot) ga `/start` bosing.
3. **Loyihani tayyorlash:**
   ```bash
   cd uy_bot
   python3 -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   ```
4. **`.env` faylini tahrirlang:**
   ```
   BOT_TOKEN=sizning_tokeningiz
   ADMIN_IDS=sizning_telegram_id_ingiz
   ```
5. **Ishga tushiring:**
   ```bash
   python3 main.py
   ```
6. Telegram’da botingizga o'ting va `/start` bosing.

Bot birinchi marta ishga tushganda `uy_bot.db` nomli SQLite fayl avtomatik yaratiladi —
alohida server yoki bulut xizmati sozlashning hojati yo'q, lekin doimiy ishlashi uchun
botni serverga (VPS) yoki masalan Railway/Render kabi xizmatga joylashtirish tavsiya etiladi.

## ⚠️ Muhim eslatmalar

- **Tarmoq**: bu muhitda (Claude ishlagan konteynerda) tashqi internetga chiqish yopiq bo'lgani
  uchun men botni haqiqiy Telegram serveriga ulab **jonli sinovdan o'tkaza olmadim** — faqat barcha
  fayllarning Python sintaksisi va mantiqiy zanjiri tekshirilgan. O'zingizning muhitingizda
  `pip install -r requirements.txt` dan so'ng albatta real tokeningiz bilan sinab ko'ring.
- **Lokatsiya bo'yicha qidiruv**: bu faqat lokatsiyasini kiritgan ijaraga beruvchilarning
  e'lonlari orasida ishlaydi (bosqichda ixtiyoriy, lekin tavsiya etiladi).
- **Tumanlar ro'yxati**: `regions.py` dagi tuman nomlari O'zbekistonning umumiy ma'lumotlariga
  asoslangan; agar sizning hududingizda aniqroq/yangilangan ro'yxat kerak bo'lsa, shu faylni
  tahrirlash kifoya — boshqa hech qaysi faylni o'zgartirish shart emas.
- **Rasm cheklovi**: Sotishda 2-10 ta, ijaraga berishda aniq 4 ta — talab qilinganidek qattiq nazorat qilinadi.

## 🔧 Keyingi qadamlar (agar xohlasangiz kengaytirsa bo'ladi)

- E'lonlarni tahrirlash (narxni o'zgartirish, rasm qo'shish)
- Sahifalash (pagination) — hozircha bitta hududdagi barcha e'lonlar ketma-ket yuboriladi
- Veb-asosidagi admin-panel (hozircha `/stats`, `/users`, `/listings` buyruqlari)
- E'lonlarni kalit so'z yoki narx oralig'i bo'yicha filtrlash

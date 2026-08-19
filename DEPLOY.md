# 🚀 Botni 24/7 ishga tushirish (deploy qilish)

Token va admin ID allaqachon `.env` fayliga kiritilgan — botni faqat serverga joylab,
doimiy ishlaydigan qilib qo'yish qoladi.

> ⚠️ **Xavfsizlik eslatmasi**: bot tokeningizni shu suhbatda menga yubordingiz. Agar bu suhbat
> boshqa birov bilan ulashilsa yoki tarixi ko'rinadigan bo'lsa, tokeningiz ham ko'rinadi.
> Ehtiyot chorasi sifatida @BotFather ga borib `/mybots` → botingiz → **API Token** →
> **Revoke current token** orqali istalgan vaqtda tokenni bekor qilib, yangisini olishingiz mumkin
> (shunda faqat `.env` dagi `BOT_TOKEN` ni yangilash kifoya, boshqa hech narsa o'zgarmaydi).

## Variant A — VPS (eng ishonchli, tavsiya etiladi)

Har qanday Linux VPS (masalan Oracle Cloud Free Tier, Timeweb, Hetzner va h.k.) ishlaydi.

```bash
# 1) Loyihani serverga yuklang (masalan scp orqali) va papkaga kiring
cd uy_bot

# 2) Virtual muhit va kutubxonalar
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate

# 3) systemd xizmati sifatida ro'yxatdan o'tkazish
sudo cp deploy/uy_bot.service /etc/systemd/system/uy_bot.service
sudo nano /etc/systemd/system/uy_bot.service   # USER va yo'llarni o'zingizga moslang

sudo systemctl daemon-reload
sudo systemctl enable uy_bot
sudo systemctl start uy_bot

# Holatini tekshirish
sudo systemctl status uy_bot

# Loglarni kuzatish
journalctl -u uy_bot -f
```

Server qayta yuklansa ham (`enable` tufayli) va bot yiqilsa ham (`Restart=always`
tufayli) avtomatik qayta ishga tushadi — bu **haqiqiy 24/7** rejim.

## Variant B — Tezkor sinov uchun (VPS bo'lmasa)

```bash
# tmux yoki screen ichida ishga tushiring, terminalni yopsangiz ham davom etadi
tmux new -s uy_bot
source venv/bin/activate
python3 main.py
# Chiqish uchun: Ctrl+B, keyin D (bot ishlashda davom etadi)
# Qaytib kirish uchun: tmux attach -t uy_bot
```

Bu variant server qayta yuklanganda yoki nosozlik chiqsa avtomatik tiklanmaydi —
uzoq muddatli 24/7 uchun **A variantini** tavsiya qilaman.

## Variant C — Bulut platformalari (Railway / Render kabi)

Agar VPS bilan ovora bo'lishni istamasangiz, Railway yoki Render kabi xizmatlarga
`uy_bot` papkasini GitHub repo qilib yuklab, Start Command sifatida
`python3 main.py` ni ko'rsatib, Environment Variables bo'limiga `.env` dagi
`BOT_TOKEN` va `ADMIN_IDS` ni kiritish orqali ham ishga tushirish mumkin.
Bunda ma'lumotlar bazasi (`uy_bot.db`) platforma qayta ishga tushganda
o'chib ketmasligi uchun **persistent disk/volume** yoqilganiga ishonch hosil qiling.

## ✅ Ishga tushgach tekshirish

1. Telegram’da botingizga `/start` yuboring — til tanlash chiqishi kerak.
2. O'zingiz (admin) uchun `/stats` buyrug'ini yuboring — statistikani ko'rsatishi kerak.
3. Bir necha test e'lon joylab, "Mening reklamalarim" bo'limidan o'chirib ko'ring.

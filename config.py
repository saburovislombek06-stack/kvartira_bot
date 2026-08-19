# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Vergul bilan ajratilgan admin Telegram ID lari: ADMIN_IDS=123456,789012
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip().isdigit()]

# Ijaraga olishda "yaqin atrofdan qidirish" radiusi (km)
NEARBY_RADIUS_KM = 10

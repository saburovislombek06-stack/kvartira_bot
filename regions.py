# -*- coding: utf-8 -*-
"""
O'zbekiston Respublikasi ma'muriy-hududiy bo'linishi:
12 ta viloyat + Toshkent shahri + Qoraqalpog'iston Respublikasi.
Har bir hudud uchun tumanlar (va shahar) ro'yxati.

Bu lug'at REGIONS o'zgaruvchisida saqlanadi:
    {region_key: {"name": {"uz": ..., "ru": ..., "kk": ..., "kaa": ...}, "districts": [...]}}

Tuman nomlari uchun ham 4 tilda tarjima berilgan (asosiylari), zarurat bo'lsa
kengaytirish oson - shunchaki DISTRICT_NAMES ga qo'shing.
"""

REGIONS = {
    "tashkent_city": {
        "name": {"uz": "Toshkent shahri", "ru": "город Ташкент",
                  "kk": "Ташкент қаласы", "kaa": "Tashkent qalasi"},
        "districts": [
            "Bektemir", "Chilonzor", "Hamza", "Mirobod", "Mirzo Ulug'bek",
            "Olmazor", "Sergeli", "Shayxontohur", "Uchtepa", "Yakkasaroy",
            "Yashnobod", "Yunusobod", "Yangihayot",
        ],
    },
    "tashkent_region": {
        "name": {"uz": "Toshkent viloyati", "ru": "Ташкентская область",
                  "kk": "Ташкент облысы", "kaa": "Tashkent oblastі"},
        "districts": [
            "Bekobod", "Bo'ka", "Bo'stonliq", "Chinoz", "Ohangaron",
            "Oqqo'rg'on", "Parkent", "Piskent", "Qibray", "Quyichirchiq",
            "Toshkent tumani", "Yuqorichirchiq", "Zangiota", "O'rtachirchiq",
            "Nurafshon shahri", "Angren shahri", "Olmaliq shahri", "Chirchiq shahri",
        ],
    },
    "andijan": {
        "name": {"uz": "Andijon viloyati", "ru": "Андижанская область",
                  "kk": "Андижан облысы", "kaa": "Andijan oblastі"},
        "districts": [
            "Andijon shahri", "Andijon tumani", "Asaka", "Baliqchi", "Bo'z",
            "Buloqboshi", "Izboskan", "Jalaquduq", "Xo'jaobod", "Qo'rg'ontepa",
            "Marhamat", "Oltinko'l", "Paxtaobod", "Shahrixon", "Ulug'nor", "Xonobod",
        ],
    },
    "bukhara": {
        "name": {"uz": "Buxoro viloyati", "ru": "Бухарская область",
                  "kk": "Бухара облысы", "kaa": "Buxara oblastі"},
        "districts": [
            "Buxoro shahri", "Buxoro tumani", "G'ijduvon", "Jondor", "Kogon",
            "Olot", "Peshku", "Qorako'l", "Qorovulbozor", "Romitan",
            "Shofirkon", "Vobkent",
        ],
    },
    "fergana": {
        "name": {"uz": "Farg'ona viloyati", "ru": "Ферганская область",
                  "kk": "Ферғана облысы", "kaa": "Fergana oblastі"},
        "districts": [
            "Farg'ona shahri", "Farg'ona tumani", "Bag'dod", "Beshariq",
            "Buvayda", "Dang'ara", "Furqat", "Qo'shtepa", "Oltiariq", "Quva",
            "Quvasoy shahri", "Rishton", "So'x", "Toshloq", "Uchko'prik",
            "O'zbekiston", "Yozyovon", "Marg'ilon shahri", "Qo'qon shahri",
        ],
    },
    "jizzakh": {
        "name": {"uz": "Jizzax viloyati", "ru": "Джизакская область",
                  "kk": "Жиззах облысы", "kaa": "Jizzax oblastі"},
        "districts": [
            "Jizzax shahri", "Jizzax tumani", "Arnasoy", "Baxmal", "Do'stlik",
            "Forish", "G'allaorol", "Mirzacho'l", "Paxtakor", "Yangiobod",
            "Zafarobod", "Zarbdor", "Zomin",
        ],
    },
    "khorezm": {
        "name": {"uz": "Xorazm viloyati", "ru": "Хорезмская область",
                  "kk": "Хорезм облысы", "kaa": "Xorezm oblastі"},
        "districts": [
            "Urganch shahri", "Urganch tumani", "Bog'ot", "Gurlan", "Hazorasp",
            "Xiva", "Xonqa", "Qo'shko'pir", "Shovot", "Yangiariq", "Yangibozor",
        ],
    },
    "namangan": {
        "name": {"uz": "Namangan viloyati", "ru": "Наманганская область",
                  "kk": "Наманган облысы", "kaa": "Namangan oblastі"},
        "districts": [
            "Namangan shahri", "Namangan tumani", "Chortoq", "Chust",
            "Kosonsoy", "Mingbuloq", "Norin", "Pop", "To'raqo'rg'on",
            "Uychi", "Uchqo'rg'on", "Yangiqo'rg'on",
        ],
    },
    "navoiy": {
        "name": {"uz": "Navoiy viloyati", "ru": "Навоийская область",
                  "kk": "Навои облысы", "kaa": "Navoiy oblastі"},
        "districts": [
            "Navoiy shahri", "Zarafshon shahri", "Karmana", "Konimex",
            "Navbahor", "Nurota", "Qiziltepa", "Tomdi", "Uchquduq", "Xatirchi",
        ],
    },
    "kashkadarya": {
        "name": {"uz": "Qashqadaryo viloyati", "ru": "Кашкадарьинская область",
                  "kk": "Қашқадария облысы", "kaa": "Qashqadaryo oblastі"},
        "districts": [
            "Qarshi shahri", "Qarshi tumani", "Chiroqchi", "Dehqonobod",
            "G'uzor", "Kasbi", "Kitob", "Koson", "Mirishkor", "Muborak",
            "Nishon", "Shahrisabz shahri", "Yakkabog'", "Kamashi",
        ],
    },
    "samarkand": {
        "name": {"uz": "Samarqand viloyati", "ru": "Самаркандская область",
                  "kk": "Самарқанд облысы", "kaa": "Samarqand oblastі"},
        "districts": [
            "Samarqand shahri", "Samarqand tumani", "Bulung'ur", "Ishtixon",
            "Jomboy", "Kattaqo'rg'on shahri", "Narpay", "Nurobod", "Oqdaryo",
            "Payariq", "Paxtachi", "Pastdarg'om", "Qo'shrabot", "Toyloq", "Urgut",
        ],
    },
    "syrdarya": {
        "name": {"uz": "Sirdaryo viloyati", "ru": "Сырдарьинская область",
                  "kk": "Сырдария облысы", "kaa": "Sirdaryo oblastі"},
        "districts": [
            "Guliston shahri", "Guliston tumani", "Boyovut", "Mirzaobod",
            "Oqoltin", "Sardoba", "Sayxunobod", "Sirdaryo", "Xovos", "Yangiyer shahri",
        ],
    },
    "surkhandarya": {
        "name": {"uz": "Surxondaryo viloyati", "ru": "Сурхандарьинская область",
                  "kk": "Сурхандария облысы", "kaa": "Surxandaryo oblastі"},
        "districts": [
            "Termiz shahri", "Termiz tumani", "Angor", "Bandixon", "Boysun",
            "Denov", "Jarqo'rg'on", "Muzrabot", "Oltinsoy", "Qiziriq",
            "Qumqo'rg'on", "Sariosiyo", "Sherobod", "Sho'rchi", "Uzun",
        ],
    },
    "karakalpakstan": {
        "name": {"uz": "Qoraqalpog'iston Respublikasi", "ru": "Республика Каракалпакстан",
                  "kk": "Қарақалпақстан Республикасы", "kaa": "Qaraqalpaqstan Respublikasi"},
        "districts": [
            "Nukus shahri", "Nukus tumani", "Amudaryo", "Beruniy", "Chimboy",
            "Ellikqal'a", "Kegeyli", "Mo'ynoq", "Qanliko'l", "Qo'ng'irot",
            "Qorao'zak", "Shumanay", "Taxtako'pir", "To'rtko'l", "Xo'jayli",
        ],
    },
}


def region_list():
    """[(key, display_order)] ro'yxati - REGIONS tartibida."""
    return list(REGIONS.keys())


def region_name(region_key: str, lang: str) -> str:
    return REGIONS[region_key]["name"].get(lang, REGIONS[region_key]["name"]["uz"])


def districts_of(region_key: str):
    return REGIONS[region_key]["districts"]

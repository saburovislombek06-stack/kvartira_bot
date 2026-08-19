# -*- coding: utf-8 -*-
"""
Foydalanuvchi qaysi tilni tanlagan bo'lishidan qat'iy nazar (uz/ru/kk/kaa),
reply-keyboard tugmalari matn sifatida keladi. Shu sabab har bir tugmani
TEXTS ichidagi barcha tarjimalar bilan solishtiruvchi kichik filtr kerak.
"""
from locales import TEXTS


def any_lang(key: str):
    """Berilgan kalitning barcha tildagi variantlari to'plamini qaytaradi."""
    return set(TEXTS[key].values())


def is_text(message_text: str, key: str) -> bool:
    return message_text in any_lang(key)

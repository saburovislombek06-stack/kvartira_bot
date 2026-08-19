# -*- coding: utf-8 -*-
"""
Botning barcha matnlari 4 tilda: uz (o'zbek), ru (rus), kk (qozoq), kaa (qoraqalpoq).
get_text(key, lang, **kwargs) orqali ishlatiladi.
"""

TEXTS = {
    "choose_language": {
        "uz": "🌐 Tilni tanlang:",
        "ru": "🌐 Выберите язык:",
        "kk": "🌐 Тілді таңдаңыз:",
        "kaa": "🌐 Tildi saylań:",
    },
    "ask_fullname": {
        "uz": "Ro'yxatdan o'tish uchun ism va familiyangizni yozing (masalan: Aziz Karimov):",
        "ru": "Для регистрации введите ваше имя и фамилию (например: Азиз Каримов):",
        "kk": "Тіркелу үшін аты-жөніңізді жазыңыз (мысалы: Азиз Каримов):",
        "kaa": "Dizimnen ótiw ushın atıńız hám familiyańızdı jazıń (mısalı: Aziz Karimov):",
    },
    "ask_phone": {
        "uz": "📱 Endi telefon raqamingizni yuboring (tugmani bosing yoki qo'lda kiriting: +998901234567):",
        "ru": "📱 Теперь отправьте ваш номер телефона (нажмите кнопку или введите вручную: +998901234567):",
        "kk": "📱 Енді телефон нөміріңізді жіберіңіз (батырманы басыңыз немесе қолмен енгізіңіз):",
        "kaa": "📱 Endi telefon nomerińizdi jiberiń (túymeni basıń yamasa qolǵa kirgiziń):",
    },
    "share_phone_btn": {
        "uz": "📱 Raqamni ulashish",
        "ru": "📱 Поделиться номером",
        "kk": "📱 Нөмірмен бөлісу",
        "kaa": "📱 Nomer menen bólisiw",
    },
    "registration_done": {
        "uz": "✅ Ro'yxatdan muvaffaqiyatli o'tdingiz, {name}!",
        "ru": "✅ Вы успешно зарегистрированы, {name}!",
        "kk": "✅ Сіз сәтті тіркелдіңіз, {name}!",
        "kaa": "✅ Siz table tabıslı dizimnen ótkiziliwińiz, {name}!",
    },
    "main_menu": {
        "uz": "🏠 Asosiy menyu. Kerakli bo'limni tanlang:",
        "ru": "🏠 Главное меню. Выберите нужный раздел:",
        "kk": "🏠 Басты мәзір. Қажетті бөлімді таңдаңыз:",
        "kaa": "🏠 Tiykarǵı menyu. Kerekli bólimdi saylań:",
    },
    "btn_sell": {
        "uz": "🏷 Uy sotish",
        "ru": "🏷 Продать дом",
        "kk": "🏷 Үй сату",
        "kaa": "🏷 Úy satıw",
    },
    "btn_buy": {
        "uz": "🛒 Uy sotib olish",
        "ru": "🛒 Купить дом",
        "kk": "🛒 Үй сатып алу",
        "kaa": "🛒 Úy satıp alıw",
    },
    "btn_rent_out": {
        "uz": "🔑 Uy ijaraga berish",
        "ru": "🔑 Сдать дом в аренду",
        "kk": "🔑 Үйді жалға беру",
        "kaa": "🔑 Úydi ijaraǵa beriw",
    },
    "btn_rent_in": {
        "uz": "🔑 Uy ijaraga olish",
        "ru": "🔑 Снять дом в аренду",
        "kk": "🔑 Үйді жалға алу",
        "kaa": "🔑 Úydi ijaraǵa alıw",
    },
    "btn_my_ads": {
        "uz": "📋 Mening reklamalarim",
        "ru": "📋 Мои объявления",
        "kk": "📋 Менің хабарландыруларым",
        "kaa": "📋 Meniń jarnamalarım",
    },
    "btn_back": {
        "uz": "⬅️ Orqaga",
        "ru": "⬅️ Назад",
        "kk": "⬅️ Артқа",
        "kaa": "⬅️ Keri",
    },
    "btn_main_menu": {
        "uz": "🏠 Asosiy menyu",
        "ru": "🏠 Главное меню",
        "kk": "🏠 Басты мәзір",
        "kaa": "🏠 Tiykarǵı menyu",
    },
    "ask_photos_sell": {
        "uz": "📸 Uy rasmlarini yuboring (kamida 2 ta, ko'pi bilan 10 ta). Yuborilgan rasmlar: {count}/10",
        "ru": "📸 Отправьте фото дома (минимум 2, максимум 10). Отправлено: {count}/10",
        "kk": "📸 Үй суреттерін жіберіңіз (кемінде 2, көбі 10). Жіберілді: {count}/10",
        "kaa": "📸 Úy súwretlerin jiberiń (eń kem degende 2, eń kóp 10). Jiberildi: {count}/10",
    },
    "ask_photos_rent_out": {
        "uz": "📸 Uy rasmlarini yuboring (4 ta rasm majburiy). Yuborilgan rasmlar: {count}/4",
        "ru": "📸 Отправьте фото дома (обязательно 4 фото). Отправлено: {count}/4",
        "kk": "📸 Үй суреттерін жіберіңіз (міндетті түрде 4 сурет). Жіберілді: {count}/4",
        "kaa": "📸 Úy súwretlerin jiberiń (mindetti túrde 4 súwret). Jiberildi: {count}/4",
    },
    "photo_added_ask_more": {
        "uz": "✅ Rasm qabul qilindi ({count}). Yana rasm yuborasizmi?",
        "ru": "✅ Фото принято ({count}). Отправить ещё фото?",
        "kk": "✅ Сурет қабылданды ({count}). Тағы сурет жібересіз бе?",
        "kaa": "✅ Súwret qabıl etildi ({count}). Jáne súwret jibересize?",
    },
    "btn_yes_more_photo": {
        "uz": "➕ Ha, yana qo'shaman",
        "ru": "➕ Да, добавлю ещё",
        "kk": "➕ Иә, тағы қосамын",
        "kaa": "➕ Awa, jáne qosaman",
    },
    "btn_no_finish_photo": {
        "uz": "✅ Yo'q, yakunlash",
        "ru": "✅ Нет, завершить",
        "kk": "✅ Жоқ, аяқтау",
        "kaa": "✅ Yoq, juwmaqlaw",
    },
    "max_photos_reached": {
        "uz": "Rasmlar soni chegarasiga yetdingiz, davom etamiz.",
        "ru": "Вы достигли лимита фото, продолжаем.",
        "kk": "Сурет саны шегіне жеттіңіз, жалғастырамыз.",
        "kaa": "Súwret sanı shegarasına jettińiz, dawam etemiz.",
    },
    "min_photos_not_reached": {
        "uz": "⚠️ Kamida {min} ta rasm yuborishingiz kerak. Yana rasm yuboring.",
        "ru": "⚠️ Нужно отправить минимум {min} фото. Отправьте ещё.",
        "kk": "⚠️ Кемінде {min} сурет жіберу керек. Тағы жіберіңіз.",
        "kaa": "⚠️ Eń kem degende {min} súwret jiberiw kerek. Jáne jiberiń.",
    },
    "ask_region": {
        "uz": "🗺 Viloyatni tanlang:",
        "ru": "🗺 Выберите область:",
        "kk": "🗺 Облысты таңдаңыз:",
        "kaa": "🗺 Oblastі saylań:",
    },
    "ask_district": {
        "uz": "🗺 Tuman/shaharni tanlang:",
        "ru": "🗺 Выберите район/город:",
        "kk": "🗺 Ауданды/қаланы таңдаңыз:",
        "kaa": "🗺 Rayon/qalanı saylań:",
    },
    "ask_price_sell": {
        "uz": "💰 Uyning narxini kiriting (so'mda, masalan: 450000000):",
        "ru": "💰 Введите цену дома (в сумах, например: 450000000):",
        "kk": "💰 Үй бағасын енгізіңіз (сумда, мысалы: 450000000):",
        "kaa": "💰 Úydiń bahasın kirgiziń (sumda, mısalı: 450000000):",
    },
    "ask_price_rent": {
        "uz": "💰 Ijara summasini kiriting (oyiga, so'mda):",
        "ru": "💰 Введите сумму аренды (в месяц, в сумах):",
        "kk": "💰 Жалдау сомасын енгізіңіз (айына, сумда):",
        "kaa": "💰 Ijara summasın kirgiziń (aylıq, sumda):",
    },
    "ask_extra_info_optional": {
        "uz": "📝 Qo'shimcha ma'lumot kiriting (ixtiyoriy). O'tkazib yuborish uchun \"O'tkazib yuborish\" tugmasini bosing:",
        "ru": "📝 Введите дополнительную информацию (необязательно). Чтобы пропустить, нажмите «Пропустить»:",
        "kk": "📝 Қосымша ақпарат енгізіңіз (міндетті емес). Өткізіп жіберу үшін «Өткізу» батырмасын басыңыз:",
        "kaa": "📝 Qosımsha maǵlıwmat kirgiziń (mindetti emes). Ótkerip jiberiw ushın «Ótkeriw» túymesin basıń:",
    },
    "btn_skip": {
        "uz": "⏭ O'tkazib yuborish",
        "ru": "⏭ Пропустить",
        "kk": "⏭ Өткізу",
        "kaa": "⏭ Ótkeriw",
    },
    "ask_contact_phone": {
        "uz": "☎️ Murojaat uchun telefon raqamingizni kiriting:",
        "ru": "☎️ Введите номер телефона для связи:",
        "kk": "☎️ Байланыс үшін телефон нөміріңізді енгізіңіз:",
        "kaa": "☎️ Baylanıs ushın telefon nomerińizdi kirgiziń:",
    },
    "ask_rent_terms": {
        "uz": "📄 Shartnoma tuziladimi, sharoitlari qanday? (qisqacha yozing):",
        "ru": "📄 Заключается ли договор, какие условия? (кратко опишите):",
        "kk": "📄 Шарт жасалады ма, шарттары қандай? (қысқаша жазыңыз):",
        "kaa": "📄 Shártnama dúzіledi me, sharayatları qanday? (qısqasha jazıń):",
    },
    "ad_published": {
        "uz": "🎉 E'loningiz muvaffaqiyatli joylandi!",
        "ru": "🎉 Ваше объявление успешно опубликовано!",
        "kk": "🎉 Хабарландыруыңыз сәтті жарияланды!",
        "kaa": "🎉 Jarnamańız tabıslı jaylastırıldı!",
    },
    "choose_region_search": {
        "uz": "Qidiruv uchun viloyatni tanlang:",
        "ru": "Выберите область для поиска:",
        "kk": "Іздеу үшін облысты таңдаңыз:",
        "kaa": "Izlew ushın oblastі saylań:",
    },
    "no_ads_found": {
        "uz": "😔 Ushbu hududda hozircha e'lonlar yo'q.",
        "ru": "😔 В этом районе пока нет объявлений.",
        "kk": "😔 Бұл аймақта әзірге хабарландырулар жоқ.",
        "kaa": "😔 Bul aymaqta házirshe jarnamalar joq.",
    },
    "ads_found": {
        "uz": "🔎 {count} ta e'lon topildi:",
        "ru": "🔎 Найдено объявлений: {count}:",
        "kk": "🔎 {count} хабарландыру табылды:",
        "kaa": "🔎 {count} jarnama tabıldı:",
    },
    "btn_extra_location": {
        "uz": "📍 Yaqin atrofdan qidirish (lokatsiya)",
        "ru": "📍 Искать поблизости (геолокация)",
        "kk": "📍 Жақын маңнан іздеу (геолокация)",
        "kaa": "📍 Jaqın átirapttan izlew (lokatsiya)",
    },
    "ask_location": {
        "uz": "📍 Lokatsiyangizni yuboring, atrofdagi 10 km radiusdagi e'lonlarni ko'rsataman:",
        "ru": "📍 Отправьте вашу геолокацию, покажу объявления в радиусе 10 км:",
        "kk": "📍 Геолокацияңызды жіберіңіз, 10 км радиустағы хабарландыруларды көрсетемін:",
        "kaa": "📍 Lokatsiyańızdı jiberiń, átirapdaǵı 10 km radiustaǵı jarnamalardı kórsetemen:",
    },
    "btn_send_location": {
        "uz": "📍 Lokatsiyani yuborish",
        "ru": "📍 Отправить геолокацию",
        "kk": "📍 Геолокацияны жіберу",
        "kaa": "📍 Lokatsiyanı jiberiw",
    },
    "my_ads_empty": {
        "uz": "Sizda hozircha faol e'lonlar yo'q.",
        "ru": "У вас пока нет активных объявлений.",
        "kk": "Сізде әзірге белсенді хабарландырулар жоқ.",
        "kaa": "Sizde házirshe belsendi jarnamalar joq.",
    },
    "my_ads_title": {
        "uz": "📋 Sizning faol e'lonlaringiz:",
        "ru": "📋 Ваши активные объявления:",
        "kk": "📋 Сіздің белсенді хабарландыруларыңыз:",
        "kaa": "📋 Sizdiń belsendi jarnamalarıńız:",
    },
    "btn_remove_ad": {
        "uz": "❌ O'chirish (sotildi/berildi)",
        "ru": "❌ Удалить (продано/сдано)",
        "kk": "❌ Жою (сатылды/берілді)",
        "kaa": "❌ Óshiriw (satıldı/berildi)",
    },
    "ad_removed": {
        "uz": "✅ E'lon o'chirildi.",
        "ru": "✅ Объявление удалено.",
        "kk": "✅ Хабарландыру жойылды.",
        "kaa": "✅ Jarnama óshirildi.",
    },
    "unknown_command": {
        "uz": "Iltimos, menyudagi tugmalardan foydalaning.",
        "ru": "Пожалуйста, используйте кнопки меню.",
        "kk": "Мәзірдегі батырмаларды пайдаланыңыз.",
        "kaa": "Meniu túymelerinen paydalanıń.",
    },
    "contact_seller": {
        "uz": "☎️ Bog'lanish uchun: {phone}\n👤 E'lon beruvchi: {name}",
        "ru": "☎️ Для связи: {phone}\n👤 Автор объявления: {name}",
        "kk": "☎️ Байланысу үшін: {phone}\n👤 Хабарландыру иесі: {name}",
        "kaa": "☎️ Baylanısıw ushın: {phone}\n👤 Jarnama iesi: {name}",
    },
    "admin_not_authorized": {
        "uz": "⛔️ Bu buyruq faqat administrator uchun.",
        "ru": "⛔️ Эта команда только для администратора.",
        "kk": "⛔️ Бұл команда тек әкімші үшін.",
        "kaa": "⛔️ Bul buyrıq tek administrator ushın.",
    },
}


def t(key: str, lang: str, **kwargs) -> str:
    """Berilgan kalit va til bo'yicha matnni qaytaradi (fallback: uz)."""
    entry = TEXTS.get(key)
    if entry is None:
        return key
    text = entry.get(lang, entry.get("uz", key))
    if kwargs:
        text = text.format(**kwargs)
    return text


LANG_NAMES = {"uz": "🇺🇿 O'zbekcha", "ru": "🇷🇺 Русский", "kk": "🇰🇿 Қазақша", "kaa": "Qaraqalpaqsha"}

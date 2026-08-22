# -*- coding: utf-8 -*-
"""
Kengaytirilgan mahalliy kontent banki.
Uslub: @alamiy_uz kanali kabi - hissiy, samimiy, ba'zan kulgili,
ba'zan chuqur. Faqat motivatsiya emas - hayotiy, jonli matn.
"""

import random

# ============================================================
# 1) MASHHUR IQTIBOSLAR - muallifi bilan
# ============================================================
IQTIBOSLAR = [
    {"matn": "Bilim - kuchdir.", "muallif": "Frensis Bekon"},
    {"matn": "O'zingni bil.", "muallif": "Suqrot"},
    {"matn": "Yashash uchun kurash - bu tabiatning qonuni.", "muallif": "Charlz Darvin"},
    {"matn": "Vaqt - eng qimmatli boylik, chunki uni qaytarib bo'lmaydi.", "muallif": "Abu Ali ibn Sino"},
    {"matn": "Ilm - go'zallikdir, uni izlagan hech qachon pushaymon bo'lmaydi.", "muallif": "Alisher Navoiy"},
    {"matn": "Kishining qadri o'z himmati bilan o'lchanadi.", "muallif": "Alisher Navoiy"},
    {"matn": "Do'stlik - ikki tan, bir jon.", "muallif": "Sharq hikmati"},
    {"matn": "Sabr - achchiq, lekin mevasi shirin.", "muallif": "Sharq maqoli"},
    {"matn": "Yaxshilik qil, daryoga tashla, baliq bilmasa, xoliq biladi.", "muallif": "O'zbek maqoli"},
    {"matn": "Kim yurса, o'zi yetar maqsadga.", "muallif": "O'zbek maqoli"},
    {"matn": "Yurak ko'zi bilan qaralgan narsa hech qachon yolg'on gapirmaydi.", "muallif": "Jaloliddin Rumiy"},
    {"matn": "Yaralaring senga yorug'lik kiradigan joy bo'lsin.", "muallif": "Jaloliddin Rumiy"},
    {"matn": "Kecha ketdi, ertasi hali yo'q, faqat bugun bor - uni yashagin.", "muallif": "Jaloliddin Rumiy"},
    {"matn": "Sevgi - ikki jonning bir tanda yashashi.", "muallif": "Aristotel"},
    {"matn": "Baxt - bu maqsad emas, yo'lning o'zi.", "muallif": "Kanfutsiy"},
    {"matn": "Kim o'zini yengsa, eng katta g'alabani qozonadi.", "muallif": "Kanfutsiy"},
    {"matn": "Hayot - bu sen band bo'lganingda boshqa rejalar tuzayotgan narsa.", "muallif": "Jon Lennon"},
    {"matn": "Kutubxona - insoniyat qalbining davolanish joyi.", "muallif": "Qadimgi Misr yozuvi"},
    {"matn": "Kim ko'p bilsa, kam gapiradi.", "muallif": "Sharq hikmati"},
    {"matn": "Tinchlik - kuchlilarning ziynati.", "muallif": "Sharq maqoli"},
    {"matn": "Insonning qadri - ilmi va odobi bilan bo'ladi, boyligi bilan emas.", "muallif": "Abu Rayhon Beruniy"},
    {"matn": "Har bir kun - yangi hayotning boshlanishi.", "muallif": "Sharq hikmati"},
    {"matn": "O'zgarish - hayotning yagona doimiy qonuni.", "muallif": "Geraklit"},
    {"matn": "Kuchli bo'lish - yiqilmaslik emas, har safar qayta turishdir.", "muallif": "Konfutsiy"},
    {"matn": "Muhabbat - ikki qalbning bitta orzu bilan yashashi.", "muallif": "Jubron Xalil Jubron"},
    {"matn": "Ozodlik - qafasda tug'ilgan qushga osmonni orzu qilishdir.", "muallif": "Jubron Xalil Jubron"},
    {"matn": "Dard chekmagan qalb hech qachon sevgini chuqur tushunmaydi.", "muallif": "Jubron Xalil Jubron"},
    {"matn": "Yaxshi so'z - sadaqadir.", "muallif": "Hadis"},
    {"matn": "Kim odamlarga rahm qilmasa, unga ham rahm qilinmaydi.", "muallif": "Hadis"},
    {"matn": "Ilm Xitoyda bo'lsa ham boring, uni izlang.", "muallif": "Hadis"},
]

# ============================================================
# 2) KUNDALIK HAZIL - hayotiy, samimiy, kulgili
# ============================================================
KUNDALIK_HAZIL = [
    "Ish kunining eng qiyin qismi - uni boshlash. Qolgani o'zi ketaveradi... yoki ketmaydi 😅",
    "Dushanba kuni ishga borish - bu ham bir turdagi jasorat.",
    "Choy ichmasdan turib \"tetikman\" deydigan odamlarga ishonmayman.",
    "Uyqu - eng arzon va eng samarali dorivor vosita, faqat vaqt yetishmaydi.",
    "Telefon batareyasi 1% qolganda ham \"hali yetadi\" deb o'ylaymiz.",
    "Ertaga qilaman deganlarim allaqachon kichik bir arxiv hosil qildi.",
    "Charchagan odam ko'proq uxlaydi, charchamagan odam ko'proq shikoyat qiladi.",
    "Bugun rejalashtirgan ishlarimning yarmi \"ertaga\" ro'yxatiga o'tdi.",
    "Issiq kunlarda eng katta orzu - konditsioner ishlaydigan xonada qolish.",
    "Hafta oxiri tez tugaydi, dushanba esa doim vaqtida keladi.",
    "Ba'zan eng katta yutuq - bugun kechikmay uyg'onish edi.",
    "Kofe ichmasdan gaplashadigan odamlarga hurmatim cheksiz.",
    "\"Besh daqiqa\" deb boshlangan tanaffus ko'pincha bir soatga cho'ziladi.",
    "Sovuq choy ichishga to'g'ri kelgan kunlarim ko'p - unutib qo'yaman doim.",
    "Yomg'irli kunlar - uydan chiqmaslik uchun eng yaxshi bahona.",
    "Har kim o'z hayotida kamida bitta \"nega buni qildim\" lahzasiga ega.",
    "Ba'zan eng katta motivatsiya - ertangi dam olish kunini eslash.",
    "Odamlar \"vaqtim yo'q\" deydi, lekin telefonni tekshirishga vaqt topadi.",
    "Uyqusizlik tunlari - eng g'alati fikrlar tug'iladigan payt.",
    "Rejalar chiroyli, hayot esa o'ziga xos yo'l tanlaydi.",
    "Kimdir \"bugun dam olaman\" deydi, aslida u ham band bo'lib qoladi.",
    "Har kuni bir xil savol: \"nima yeyman?\" - javob doim qiyin.",
    "Sovg'a olishdan ko'ra sovg'a berish qiziqroq, deb aytishadi - to'g'ri ekan.",
    "Tanish odam ko'chada ko'rinsa, birdan telefon bilan \"band\" bo'lib qolamiz.",
    "Erta uxlayman deb va'da berib, yana kech uxlash - bu ham bir an'ana.",
]

# ============================================================
# 3) SHE'RIY SATRLAR - qisqa, hissiy, original
# ============================================================
SHERIY_SATRLAR = [
    "Sog'inch —\nbu yo'qlikning\neng baland ovozi.\nU jim turadi,\nlekin qalbda\nqattiq jaranglaydi.",
    "Har kuni bir bahona\ntopaman seni eslash uchun,\naslida esa\nseni unutmaganman\nhech qachon.",
    "Kuz barglari kabi\nto'kilgan orzularim,\nlekin ildizim\nhali ham umidga\nbog'langan.",
    "Sensiz kunlar\nuzun tuyuladi,\nlekin sen bilan\no'tgan lahzalar\nhamon yorug'.",
    "Yurak — kichkina uy,\nunda hamma sig'maydi,\nlekin sen doim\neng issiq xonada\nturasan.",
    "Kutish — bu ham\nbir turdagi sevgi,\nsabr bilan yozilgan\ntugallanmagan\nxat kabi.",
    "Har bir tong\nseni eslatadi,\nquyosh chiqishi ham\nsening tabassuming\nkabi iliq.",
    "Uzoqlik — masofa emas,\nbu ikki qalb orasidagi\njimlik, xolos.",
    "Ba'zan sog'inch\nso'zga sig'maydi,\nfaqat sukunatda\nyashab qoladi.",
    "Sevgi — ko'rilmagan\nyo'lda yurish,\nlekin har qadam\nishonch bilan\nbosiladi.",
    "Yolg'izlik kechalari\nyulduzlarga gapiraman,\nulardan biri\nseni eshitib\nqolar deb umid qilib.",
    "Har bir xotira —\nqalbimda saqlangan\nkichik chiroq,\nzulmatda ham\nyorug' beradi.",
]

# ============================================================
# 4) FUNKSIYALAR
# ============================================================

def get_random_iqtibos():
    """Tasodifiy iqtibos + muallif"""
    item = random.choice(IQTIBOSLAR)
    return f'"{item["matn"]}"\n\n— {item["muallif"]}'


def get_random_hazil():
    """Tasodifiy kundalik hazil/hayotiy gap"""
    return random.choice(KUNDALIK_HAZIL)


def get_random_sheriy():
    """Tasodifiy she'riy satr"""
    return random.choice(SHERIY_SATRLAR)


def get_mixed_content():
    """
    Har chaqiruvda tasodifiy turdagi kontent qaytaradi:
    iqtibos, hazil yoki she'riy satr - xilma-xillik uchun
    """
    choice = random.choice(["iqtibos", "hazil", "sheriy"])
    if choice == "iqtibos":
        return get_random_iqtibos()
    elif choice == "hazil":
        return get_random_hazil()
    else:
        return get_random_sheriy()


if __name__ == "__main__":
    print("=== IQTIBOS namunasi ===")
    print(get_random_iqtibos())
    print("\n=== HAZIL namunasi ===")
    print(get_random_hazil())
    print("\n=== SHE'RIY namunasi ===")
    print(get_random_sheriy())
    print(f"\nJami: {len(IQTIBOSLAR)} iqtibos, {len(KUNDALIK_HAZIL)} hazil, {len(SHERIY_SATRLAR)} she'riy satr")

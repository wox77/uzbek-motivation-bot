# -*- coding: utf-8 -*-
"""
Kengaytirilgan mahalliy kontent banki.
Uslub: @alamiy_uz kanali kabi - hissiy, samimiy, ba'zan kulgili,
ba'zan chuqur. Faqat motivatsiya emas - hayotiy, jonli matn.
"""

import random

# ============================================================
# 1) TEKSHIRILGAN IQTIBOSLAR - muallifi va manbasi bilan
# ============================================================
IQTIBOSLAR = [
    {
        "matn": "Odamiy ersang, demagil odami, onikim yo‘q xalq g‘amidin g‘ami.",
        "muallif": "Alisher Navoiy",
        "manba": "Hayrat ul-abror",
        "url": "https://kutubxonachi.uz/media/books/hayrat-ul-abror_kutubxonachi.uz.pdf",
    },
    {
        "matn": "Yaxshi insonni ko‘rsang, unga tenglashishga intil; yomonini ko‘rsang, o‘zingni tekshir.",
        "muallif": "Konfutsiy",
        "manba": "Hikmatlar kitobi, 4:17",
        "url": "https://www.analects.net/analects/4-li-ren/4-jian-xian/",
    },
    {
        "matn": "O‘zingga ravo ko‘rmagan narsani boshqalarga ham ravo ko‘rma.",
        "muallif": "Konfutsiy",
        "manba": "Hikmatlar kitobi, 15:24",
        "url": "https://www.analects.net/analects/15-wei-ling-gong/15-gong-wen",
    },
    {
        "matn": "Ming li yo‘l ham oyoq ostingdan boshlanadi.",
        "muallif": "Laozi",
        "manba": "Dao De Jing, 64-bob",
        "url": "https://laozi-taoteching.org/en/chapters/64",
    },
    {
        "matn": "Aql to‘siqni yordamga aylantiradi; yo‘ldagi g‘ov ham shu yo‘lda olg‘a siljishga ko‘mak beradi.",
        "muallif": "Mark Avreliy",
        "manba": "O‘ylar, 5-kitob, 20-qism",
        "url": "https://classics.mit.edu/Antoninus/meditations.5.five.html",
    },
    {
        "matn": "Ba’zi narsalar bizning ixtiyorimizda, ba’zilari esa yo‘q. O‘z fikrimiz va harakatimiz ixtiyorimizdadir.",
        "muallif": "Epiktet",
        "manba": "Enxiridion, 1-qism",
        "url": "https://classics.mit.edu/Epictetus/epicench.html",
    },
    {
        "matn": "Bizni narsalarning o‘zi emas, ular haqidagi qarashlarimiz bezovta qiladi.",
        "muallif": "Epiktet",
        "manba": "Enxiridion, 5-qism",
        "url": "https://classics.mit.edu/Epictetus/epicench.html",
    },
    {
        "matn": "Ko‘pincha biz haqiqatda emas, tasavvurimizda ko‘proq azob chekamiz.",
        "muallif": "Seneka",
        "manba": "Lutsiliyga maktublar, 13-maktub, 4-qism",
        "url": "https://thestoiclibrary.com/letters/13#section-4",
    },
    {
        "matn": "Yaxshi-yomon degan narsa yo‘q, uni fikrimiz shunday qiladi.",
        "muallif": "Uilyam Shekspir",
        "manba": "Hamlet, 2-parda, 2-sahna",
        "url": "https://www.folger.edu/explore/shakespeares-works/hamlet/read/2/2",
    },
    {
        "matn": "Ayb yulduzlarda emas, o‘zimizda.",
        "muallif": "Uilyam Shekspir",
        "manba": "Yuliy Sezar, 1-parda, 2-sahna",
        "url": "https://www.folger.edu/explore/shakespeares-works/julius-caesar/read/1/2",
    },
    {
        "matn": "Hayot hech birimiz uchun oson emas. Xo‘sh, nima bo‘pti? Matonat va eng avvalo, o‘zimizga ishonch kerak. Bizda bir iste’dod borligiga, unga erishishimiz kerakligiga ishonishimiz lozim.",
        "muallif": "Mari Kyuri",
        "manba": "“Marie Curie: In her own words”",
        "url": "https://www.mariecurie.org.uk/about-us/our-history/marie-curie-the-scientist",
    },
    {
        "matn": "Darding — tushunchangni o‘rab turgan qobiqning yorilishidir.",
        "muallif": "Xalil Jubron",
        "manba": "Payg‘ambar, “Dard haqida”",
        "url": "https://www.gutenberg.org/files/58585/58585-h/58585-h.htm#link60",
    },
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

def get_random_iqtibos_item(exclude_texts=None):
    """Manbasi ko‘rsatilgan tasodifiy iqtibos yozuvini qaytaradi."""
    excluded = set(exclude_texts or ())
    available = [item for item in IQTIBOSLAR if item["matn"] not in excluded]
    return random.choice(available or IQTIBOSLAR)


def format_iqtibos(item):
    """Iqtibosni muallif va asar nomi bilan ko‘rsatadi."""
    return f'“{item["matn"]}”\n\n— {item["muallif"]}\n📚 {item["manba"]}'


def get_random_iqtibos():
    """Tasodifiy iqtibosni muallif va manbasi bilan qaytaradi."""
    return format_iqtibos(get_random_iqtibos_item())


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

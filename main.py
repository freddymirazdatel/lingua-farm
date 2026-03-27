import flet as ft
import asyncio
import random

def main(page: ft.Page):
    # --- SƏHİFƏ AYARLARI ---
    page.title = "Lingua Farm"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 400
    page.window_height = 800
    page.padding = 0
    page.bgcolor = "#f5f5f5"

    # --- OYUNUN YADDAŞI (STATE) ---
    state = {
        "coins": 100,
        "lives": 3,
        "exp": 0,          # 100 olanda Level Up
        "level": 1,
        "current_step": 1,
        "word_index": 0,   # Step içində neçənci sualdadır (0-dan 9-a qədər)
        "unlocked_plots": 1, # Başlanğıcda 1 torpaq açıqdır
        "sound": True,
        "vibration": True
    }

    # --- SÖZLƏR BAZASI (Nümunə - Bura 200 sözü əlavə edəcəksən) ---
    # Hər Step-də 10 söz olacaq.
    DATA = {
        1: [ # Step 1
            {"word": "APPLE", "correct": "alma", "options": ["alma", "armud", "banan"]},
            {"word": "BOOK", "correct": "kitab", "options": ["kitab", "dəftər", "qələm"]},
            {"word": "WATER", "correct": "su", "options": ["su", "çay", "süd"]},
            {"word": "SUN", "correct": "günəş", "options": ["günəş", "ay", "ulduz"]},
            {"word": "CAR", "correct": "maşın", "options": ["maşın", "avtobus", "qatar"]},
            {"word": "HOUSE", "correct": "ev", "options": ["ev", "bina", "çadır"]},
            {"word": "DOG", "correct": "it", "options": ["it", "pişik", "quş"]},
            {"word": "TREE", "correct": "ağac", "options": ["ağac", "gül", "kol"]},
            {"word": "FIRE", "correct": "od", "options": ["od", "su", "torpaq"]},
            {"word": "BREAD", "correct": "çörək", "options": ["çörək", "yağ", "pendir"]}
        ],        2: [ # Step 2
            {"word": "CAT", "correct": "pişik", "options": ["pişik", "it", "at"]},
            {"word": "MILK", "correct": "süd", "options": ["süd", "su", "şirə"]},
            {"word": "DOOR", "correct": "qapı", "options": ["qapı", "pəncərə", "divar"]},
            {"word": "BIRD", "correct": "quş", "options": ["quş", "balıq", "böcək"]},
            {"word": "TABLE", "correct": "masa", "options": ["masa", "stul", "şkaf"]},
            {"word": "PEN", "correct": "qələm", "options": ["qələm", "dəftər", "pozan"]},
            {"word": "MOON", "correct": "ay", "options": ["ay", "günəş", "ulduz"]},
            {"word": "FLOWER", "correct": "gül", "options": ["gül", "ağac", "ot"]},
            {"word": "SHOE", "correct": "ayaqqabı", "options": ["ayaqqabı", "corab", "şalvar"]},
            {"word": "ROAD", "correct": "yol", "options": ["yol", "körpü", "küçə"]}
        ],        3: [ # Step 3 (Rənglər və Təbiət)
            {"word": "RED", "correct": "qırmızı", "options": ["qırmızı", "yaşıl", "mavi"]},
            {"word": "BLUE", "correct": "mavi", "options": ["mavi", "sarı", "qara"]},
            {"word": "GREEN", "correct": "yaşıl", "options": ["yaşıl", "boz", "qırmızı"]},
            {"word": "YELLOW", "correct": "sarı", "options": ["sarı", "narıncı", "ağ"]},
            {"word": "BLACK", "correct": "qara", "options": ["qara", "qəhvəyi", "göy"]},
            {"word": "WHITE", "correct": "ağ", "options": ["ağ", "çəhrayı", "boz"]},
            {"word": "SKY", "correct": "səma", "options": ["səma", "yer", "dəniz"]},
            {"word": "STAR", "correct": "ulduz", "options": ["ulduz", "ay", "günəş"]},
            {"word": "RAIN", "correct": "yağış", "options": ["yağış", "qar", "külək"]},
            {"word": "SNOW", "correct": "qar", "options": ["qar", "duman", "dolu"]}
        ],
        4: [ # Step 4 (Ev və Otaqlar)
            {"word": "BED", "correct": "çarpayı", "options": ["çarpayı", "stul", "masa"]},
            {"word": "CHAIR", "correct": "stul", "options": ["stul", "divan", "kreslo"]},
            {"word": "WINDOW", "correct": "pəncərə", "options": ["pəncərə", "qapı", "dam"]},
            {"word": "WALL", "correct": "divar", "options": ["divar", "döşəmə", "tavan"]},
            {"word": "KITCHEN", "correct": "mətbəx", "options": ["mətbəx", "hamam", "otaq"]},
            {"word": "LAMP", "correct": "lampa", "options": ["lampa", "şəkil", "saat"]},
            {"word": "CLOCK", "correct": "saat", "options": ["saat", "telefon", "televizor"]},
            {"word": "KEY", "correct": "açar", "options": ["açar", "kilid", "qutu"]},
            {"word": "SOAP", "correct": "sabun", "options": ["sabun", "şampun", "dəsmal"]},
            {"word": "MIRROR", "correct": "güzgü", "options": ["güzgü", "daraq", "şüşə"]}
        ],
        5: [ # Step 5 (Ailə və İnsanlar)
            {"word": "MOTHER", "correct": "ana", "options": ["ana", "bacı", "bibi"]},
            {"word": "FATHER", "correct": "ata", "options": ["ata", "qardaş", "əmi"]},
            {"word": "BROTHER", "correct": "qardaş", "options": ["qardaş", "oğul", "nəvə"]},
            {"word": "SISTER", "correct": "bacı", "options": ["bacı", "qız", "xala"]},
            {"word": "BABY", "correct": "körpə", "options": ["körpə", "uşaq", "gənc"]},
            {"word": "MAN", "correct": "kişi", "options": ["kişi", "qadın", "oğlan"]},
            {"word": "WOMAN", "correct": "qadın", "options": ["qadın", "qız", "nənə"]},
            {"word": "FRIEND", "correct": "dost", "options": ["dost", "qonşu", "düşmən"]},
            {"word": "TEACHER", "correct": "müəllim", "options": ["müəllim", "şagird", "həkim"]},
            {"word": "DOCTOR", "correct": "həkim", "options": ["həkim", "polis", "sürücü"]}
        ],
        6: [ # Step 6 (Bədən Üzvləri)
            {"word": "HEAD", "correct": "baş", "options": ["baş", "əzələ", "sümük"]},
            {"word": "EYE", "correct": "göz", "options": ["göz", "qulaq", "burun"]},
            {"word": "EAR", "correct": "qulaq", "options": ["qulaq", "dil", "diş"]},
            {"word": "NOSE", "correct": "burun", "options": ["burun", "çənə", "alın"]},
            {"word": "MOUTH", "correct": "ağız", "options": ["ağız", "dodaq", "boğaz"]},
            {"word": "HAND", "correct": "əl", "options": ["əl", "barmaq", "bilək"]},
            {"word": "FOOT", "correct": "ayaq", "options": ["ayaq", "diz", "topuq"]},
            {"word": "HAIR", "correct": "saç", "options": ["saç", "qaş", "kirpik"]},
            {"word": "FACE", "correct": "üz", "options": ["üz", "boyun", "çiyin"]},
            {"word": "HEART", "correct": "ürək", "options": ["ürək", "ağciyər", "mədə"]}
        ],
        7: [ # Step 7 (Geyim və Əşyalar)
            {"word": "SHIRT", "correct": "köynək", "options": ["köynək", "şalvar", "paltar"]},
            {"word": "PANTS", "correct": "şalvar", "options": ["şalvar", "yubka", "şort"]},
            {"word": "HAT", "correct": "papaq", "options": ["papaq", "şərf", "əlcək"]},
            {"word": "BAG", "correct": "çanta", "options": ["çanta", "pulqabı", "kisə"]},
            {"word": "WATCH", "correct": "saat", "options": ["saat", "üzük", "sırğa"]},
            {"word": "GLASSES", "correct": "eynək", "options": ["eynək", "linza", "maska"]},
            {"word": "UMBRELLA", "correct": "çətir", "options": ["çətir", "yağışlıq", "papaq"]},
            {"word": "KNIFE", "correct": "bıçaq", "options": ["bıçaq", "qaşıq", "çəngəl"]},
            {"word": "SPOON", "correct": "qaşıq", "options": ["qaşıq", "boşqab", "stəkan"]},
            {"word": "FORK", "correct": "çəngəl", "options": ["çəngəl", "tava", "qazan"]}
        ],
        8: [ # Step 8 (Heyvanlar 2)
            {"word": "HORSE", "correct": "at", "options": ["at", "eşşək", "dəvə"]},
            {"word": "COW", "correct": "inək", "options": ["inək", "öküz", "camış"]},
            {"word": "SHEEP", "correct": "qoyun", "options": ["qoyun", "keçi", "quzu"]},
            {"word": "LION", "correct": "şir", "options": ["şir", "pələng", "canavar"]},
            {"word": "BEAR", "correct": "ayı", "options": ["ayı", "tülkü", "dovşan"]},
            {"word": "FISH", "correct": "balıq", "options": ["balıq", "balina", "delfin"]},
            {"word": "SNAKE", "correct": "ilan", "options": ["ilan", "kərtənkələ", "qurbağa"]},
            {"word": "MOUSE", "correct": "siçan", "options": ["siçan", "sincab", "siçovul"]},
            {"word": "MONKEY", "correct": "meymun", "options": ["meymun", "fil", "zürafə"]},
            {"word": "ELEPHANT", "correct": "fil", "options": ["fil", "kərgədan", "hippopotam"]}
        ],
        9: [ # Step 9 (Nəqliyyat və Şəhər)
            {"word": "PLANE", "correct": "təyyarə", "options": ["təyyarə", "helikopter", "raket"]},
            {"word": "SHIP", "correct": "gəmi", "options": ["gəmi", "qayıq", "sualtı"]},
            {"word": "TRAIN", "correct": "qatar", "options": ["qatar", "metro", "tramvay"]},
            {"word": "BIKE", "correct": "velosiped", "options": ["velosiped", "motosiklet", "skuter"]},
            {"word": "STREET", "correct": "küçə", "options": ["küçə", "yol", "prospekt"]},
            {"word": "PARK", "correct": "park", "options": ["park", "bağ", "meydan"]},
            {"word": "SHOP", "correct": "mağaza", "options": ["mağaza", "bazar", "apteka"]},
            {"word": "BANK", "correct": "bank", "options": ["bank", "ofis", "muzey"]},
            {"word": "CINEMA", "correct": "kino", "options": ["kino", "teatr", "sirk"]},
            {"word": "STATION", "correct": "stansiya", "options": ["stansiya", "dayanacaq", "liman"]}
        ],
        10: [ # Step 10 (Meyvələr və Tərəvəzlər)
            {"word": "BANANA", "correct": "banan", "options": ["banan", "limon", "ananas"]},
            {"word": "ORANGE", "correct": "portağal", "options": ["portağal", "mandalin", "qreypfrut"]},
            {"word": "GRAPE", "correct": "üzüm", "options": ["üzüm", "gilas", "çiyələk"]},
            {"word": "POTATO", "correct": "kartof", "options": ["kartof", "soğan", "sarımsaq"]},
            {"word": "TOMATO", "correct": "pomidor", "options": ["pomidor", "xiyar", "bibər"]},
            {"word": "CARROT", "correct": "kök", "options": ["kök", "çuğundur", "turp"]},
            {"word": "EGG", "correct": "yumurta", "options": ["yumurta", "pendir", "yağ"]},
            {"word": "SUGAR", "correct": "şəkər", "options": ["şəkər", "duz", "istiot"]},
            {"word": "TEA", "correct": "çay", "options": ["çay", "qəhvə", "kakao"]},
            {"word": "MEAT", "correct": "ət", "options": ["ət", "toyuq", "balıq"]}
        ],
  
          11: [ # Step 11 (Təbiət Hadisələri)
            {"word": "THUNDER", "correct": "ildırım", "options": ["ildırım", "külək", "bulud"]},
            {"word": "WIND", "correct": "külək", "options": ["külək", "günəş", "yağış"]},
            {"word": "CLOUD", "correct": "bulud", "options": ["bulud", "ulduz", "duman"]},
            {"word": "FOG", "correct": "duman", "options": ["duman", "qar", "dolu"]},
            {"word": "STORM", "correct": "fırtına", "options": ["fırtına", "dalğa", "sel"]},
            {"word": "WAVE", "correct": "dalğa", "options": ["dalğa", "qum", "sahil"]},
            {"word": "BEACH", "correct": "sahil", "options": ["sahil", "dağ", "meşə"]},
            {"word": "FOREST", "correct": "meşə", "options": ["meşə", "çöl", "bağ"]},
            {"word": "MOUNTAIN", "correct": "dağ", "options": ["dağ", "təpə", "dərə"]},
            {"word": "ISLAND", "correct": "ada", "options": ["ada", "qitə", "ölkə"]}
        ],
        12: [ # Step 12 (Zaman və Təqvim)
            {"word": "MORNING", "correct": "səhər", "options": ["səhər", "günorta", "axşam"]},
            {"word": "AFTERNOON", "correct": "günorta", "options": ["günorta", "gecə", "səhər"]},
            {"word": "EVENING", "correct": "axşam", "options": ["axşam", "səhər", "gecə"]},
            {"word": "NIGHT", "correct": "gecə", "options": ["gecə", "gün", "saat"]},
            {"word": "WEEK", "correct": "həftə", "options": ["həftə", "ay", "il"]},
            {"word": "MONTH", "correct": "ay", "options": ["ay", "həftə", "gün"]},
            {"word": "YEAR", "correct": "il", "options": ["il", "əsır", "mövsüm"]},
            {"word": "TODAY", "correct": "bu gün", "options": ["bu gün", "dünən", "sabah"]},
            {"word": "YESTERDAY", "correct": "dünən", "options": ["dünən", "bu gün", "sabah"]},
            {"word": "TOMORROW", "correct": "sabah", "options": ["sabah", "dünən", "bu gün"]}
        ],
        13: [ # Step 13 (Məktəb və Təhsil)
            {"word": "STUDENT", "correct": "şagird", "options": ["şagird", "müəllim", "direktor"]},
            {"word": "PAPER", "correct": "kağız", "options": ["kağız", "qələm", "kitab"]},
            {"word": "PENCIL", "correct": "karandaş", "options": ["karandaş", "rəng", "fırça"]},
            {"word": "ERASER", "correct": "pozan", "options": ["pozan", "xətkeş", "yonan"]},
            {"word": "RULER", "correct": "xətkeş", "options": ["xətkeş", "pergar", "qovluq"]},
            {"word": "CLASS", "correct": "sinif", "options": ["sinif", "məktəb", "kurs"]},
            {"word": "LESSON", "correct": "dərs", "options": ["dərs", "imtihan", "tapşırıq"]},
            {"word": "EXAM", "correct": "imtahan", "options": ["imtahan", "sual", "cavab"]},
            {"word": "QUESTION", "correct": "sual", "options": ["sual", "cavab", "səhv"]},
            {"word": "ANSWER", "correct": "cavab", "options": ["cavab", "sual", "düz"]}
        ],
        14: [ # Step 14 (Hisslər və Emosiyalar)
            {"word": "HAPPY", "correct": "xoşbəxt", "options": ["xoşbəxt", "qəmli", "əsəbi"]},
            {"word": "SAD", "correct": "qəmli", "options": ["qəmli", "şən", "qorxmuş"]},
            {"word": "ANGRY", "correct": "əsəbi", "options": ["əsəbi", "sakit", "yorğun"]},
            {"word": "TIRED", "correct": "yorğun", "options": ["yorğun", "gümrah", "yuxulu"]},
            {"word": "HUNGRY", "correct": "acıqmış", "options": ["acıqmış", "tox", "susuz"]},
            {"word": "THIRSTY", "correct": "susuz", "options": ["susuz", "tox", "acıqmış"]},
            {"word": "BRAVE", "correct": "cəsur", "options": ["cəsur", "qorxaq", "tənbəl"]},
            {"word": "AFRAID", "correct": "qorxmuş", "options": ["qorxmuş", "şad", "təəccüblü"]},
            {"word": "FUNNY", "correct": "məzəli", "options": ["məzəli", "ciddi", "maraqlı"]},
            {"word": "QUICK", "correct": "sürətli", "options": ["sürətli", "yavaş", "ağır"]}
        ],
        15: [ # Step 15 (İş və Peşələr 2)
            {"word": "POLICE", "correct": "polis", "options": ["polis", "əsgər", "yanğınsöndürən"]},
            {"word": "CHEF", "correct": "aşpaz", "options": ["aşpaz", "ofisiant", "satıcı"]},
            {"word": "PILOT", "correct": "pilot", "options": ["pilot", "kaptan", "sürücü"]},
            {"word": "DENTIST", "correct": "diş həkimi", "options": ["diş həkimi", "həkim", "tibb bacısı"]},
            {"word": "FARMER", "correct": "fermer", "options": ["fermer", "bağban", "çoban"]},
            {"word": "ARTIST", "correct": "rəssam", "options": ["rəssam", "musiqiçi", "aktyor"]},
            {"word": "SINGER", "correct": "müğənni", "options": ["müğənni", "rəqqas", "yazıçı"]},
            {"word": "WORKER", "correct": "fəhlə", "options": ["fəhlə", "mühəndis", "memar"]},
            {"word": "MANAGER", "correct": "menecer", "options": ["menecer", "direktor", "katib"]},
            {"word": "BARRISTER", "correct": "vəkil", "options": ["vəkil", "hakim", "jurnalist"]}
        ],
        16: [ # Step 16 (Hərəkətlər / Feillər 1)
            {"word": "EAT", "correct": "yemək", "options": ["yemək", "içmək", "yatmaq"]},
            {"word": "DRINK", "correct": "içmək", "options": ["içmək", "yemək", "bişirmək"]},
            {"word": "SLEEP", "correct": "yatmaq", "options": ["yatmaq", "oyanmaq", "durmaq"]},
            {"word": "RUN", "correct": "qaçmaq", "options": ["qaçmaq", "yerimək", "tullanmaq"]},
            {"word": "WALK", "correct": "yerimək", "options": ["yerimək", "qaçmaq", "oturmaq"]},
            {"word": "SIT", "correct": "oturmaq", "options": ["oturmaq", "durmaq", "uzanmaq"]},
            {"word": "READ", "correct": "oxumaq", "options": ["oxumaq", "yazmaq", "danışmaq"]},
            {"word": "WRITE", "correct": "yazmaq", "options": ["yazmaq", "oxumaq", "dinləmək"]},
            {"word": "LISTEN", "correct": "dinləmək", "options": ["dinləmək", "baxmaq", "görmək"]},
            {"word": "LOOK", "correct": "baxmaq", "options": ["baxmaq", "eşitmək", "toxunmaq"]}
        ],
        17: [ # Step 17 (Hərəkətlər / Feillər 2)
            {"word": "OPEN", "correct": "açmaq", "options": ["açmaq", "bağlamaq", "vurmaq"]},
            {"word": "CLOSE", "correct": "bağlamaq", "options": ["bağlamaq", "açmaq", "itələmək"]},
            {"word": "GIVE", "correct": "vermək", "options": ["vermək", "almaq", "tutmaq"]},
            {"word": "TAKE", "correct": "almaq", "options": ["almaq", "vermək", "atmaq"]},
            {"word": "BUY", "correct": "satın almaq", "options": ["satın almaq", "satmaq", "paylamaq"]},
            {"word": "SELL", "correct": "satmaq", "options": ["satmaq", "almaq", "dəyişmək"]},
            {"word": "PLAY", "correct": "oynamaq", "options": ["oynamaq", "oxumaq", "rəqs etmək"]},
            {"word": "SING", "correct": "oxumaq(mahnı)", "options": ["oxumaq(mahnı)", "ağlamaq", "gülmək"]},
            {"word": "LAUGH", "correct": "gülmək", "options": ["gülmək", "ağlamaq", "təbəssüm"]},
            {"word": "CRY", "correct": "ağlamaq", "options": ["ağlamaq", "gülmək", "qışqırmaq"]}
        ],
        18: [ # Step 18 (Sifətlər / Təsvirlər)
            {"word": "BIG", "correct": "böyük", "options": ["böyük", "kiçik", "orta"]},
            {"word": "SMALL", "correct": "kiçik", "options": ["kiçik", "böyük", "nəhəng"]},
            {"word": "TALL", "correct": "hündür", "options": ["hündür", "alçaq", "qısa"]},
            {"word": "SHORT", "correct": "qısa", "options": ["qısa", "uzun", "geniş"]},
            {"word": "HOT", "correct": "isti", "options": ["isti", "soyuq", "ilıq"]},
            {"word": "COLD", "correct": "soyuq", "options": ["soyuq", "isti", "sərin"]},
            {"word": "NEW", "correct": "yeni", "options": ["yeni", "köhnə", "təzə"]},
            {"word": "OLD", "correct": "köhnə", "options": ["köhnə", "yeni", "müasir"]},
            {"word": "FAST", "correct": "sürətli", "options": ["sürətli", "yavaş", "sakit"]},
            {"word": "SLOW", "correct": "yavaş", "options": ["yavaş", "iti", "cəld"]}
        ],
        19: [ # Step 19 (Mətbəx və Qidalanma 2)
            {"word": "BOWL", "correct": "kasa", "options": ["kasa", "boşqab", "stəkan"]},
            {"word": "PLATE", "correct": "boşqab", "options": ["boşqab", "qaşıq", "tava"]},
            {"word": "CUP", "correct": "fincan", "options": ["fincan", "şüşə", "qazan"]},
            {"word": "GLASS", "correct": "stəkan", "options": ["stəkan", "bardaq", "küp"]},
            {"word": "SOUP", "correct": "şorba", "options": ["şorba", "salat", "kabab"]},
            {"word": "RICE", "correct": "düyü", "options": ["düyü", "makaron", "qarğıdalı"]},
            {"word": "SALT", "correct": "duz", "options": ["duz", "şəkər", "bibər"]},
            {"word": "JUICE", "correct": "şirə", "options": ["şirə", "su", "çəy"]},
            {"word": "FRUIT", "correct": "meyvə", "options": ["meyvə", "tərəvəz", "göyərti"]},
            {"word": "VEGETABLE", "correct": "tərəvəz", "options": ["tərəvəz", "meyvə", "ət"]}
        ],
        20: [ # Step 20 (Yekun və Qarışıq)
            {"word": "MONEY", "correct": "pul", "options": ["pul", "qızıl", "gümüş"]},
            {"word": "GIFT", "correct": "hədiyyə", "options": ["hədiyyə", "qutu", "bağlama"]},
            {"word": "WORLD", "correct": "dünya", "options": ["dünya", "ölkə", "şəhər"]},
            {"word": "PEOPLE", "correct": "insanlar", "options": ["insanlar", "uşaqlar", "qocalar"]},
            {"word": "LIFE", "correct": "həyat", "options": ["həyat", "ölüm", "yuxu"]},
            {"word": "TIME", "correct": "zaman", "options": ["zaman", "saat", "dəqiqə"]},
            {"word": "NEWS", "correct": "xəbərlər", "options": ["xəbərlər", "qəzet", "jurnal"]},
            {"word": "HELP", "correct": "kömək", "options": ["kömək", "ziyan", "xeyir"]},
            {"word": "WORK", "correct": "iş", "options": ["iş", "istirahət", "əyləncə"]},
            {"word": "GAME", "correct": "oyun", "options": ["oyun", "dərs", "məşq"]}
        ],
  
        # Step 2, 3, 4... bura əlavə edəcəksən
    }

    # Əgər bazada step yoxdursa, xəta verməsin deyə dummy data (test üçün)
    for i in range(2, 21):
        if i not in DATA:
            DATA[i] = [{"word": f"WORD {i}-{j}", "correct": "düz", "options": ["düz", "səhv1", "səhv2"]} for j in range(10)]

    # --- ÜST PANEL (Status Bar: Level, EXP, Lives, Coins) ---
    top_bar = ft.Container(
        content=ft.Row([
            ft.Text(f"Lv. {state['level']}", weight="bold", size=16, color="green800"),
            ft.ProgressBar(value=state["exp"]/100, width=120, color="green", bgcolor="green200"),
            ft.Row([
                ft.Text(f"❤️ {state['lives']}", weight="bold", color="red"),
                ft.Text(f"💰 {state['coins']}", weight="bold", color="orange800")
            ], spacing=10)
        ], alignment="spaceBetween"),
        padding=10, bgcolor="white", shadow=ft.BoxShadow(blur_radius=5, color="black12")
    )

    def update_top_bar():
        top_bar.content.controls[0].value = f"Lv. {state['level']}"
        top_bar.content.controls[1].value = state["exp"] / 100
        top_bar.content.controls[2].controls[0].value = f"❤️ {state['lives']}"
        top_bar.content.controls[2].controls[1].value = f"💰 {state['coins']}"
        page.update()

    # --- 1. SPLASH SCREEN (Açılış Ekranı) ---
    async def show_splash():
        page.controls.clear()
        splash = ft.Container(
            content=ft.Column([
                ft.Icon(ft.icons.AGRICULTURE, size=120, color="#7db343"),
                ft.Text("LINGUA FARM", size=36, weight="bold", color="#5d4037"),
                ft.Text("Oynayaraq Öyrən", size=16, italic=True, color="grey"),
                ft.Divider(height=30, color="transparent"),
                ft.ProgressBar(width=200, color="#7db343", bgcolor="#eeeeee"),
                ft.Text("Yüklənir...", size=14, color="grey")
            ], alignment="center", horizontal_alignment="center"),
            expand=True, bgcolor="#fdfdfd"
        )
        page.add(splash)
        await asyncio.sleep(2.5) # Yüklənmə effekti
        show_main_menu()

    # --- 2. ANA MENYU ---
    def show_main_menu():
        page.controls.clear()
        page.bgcolor = "#e8f5e9" # Açıq yaşıl fon
        
        menu_col = ft.Column([
            ft.Text("ANA MENYU", size=30, weight="bold", color="#2e7d32"),
            ft.Divider(height=20, color="transparent"),
            menu_btn("Mənim Bağım", ft.icons.GRASS, "#7db343", show_farm),
            menu_btn("Yeni Sözlər", ft.icons.SCHOOL, "#ff9800", start_game),
            menu_btn("Təkrarlama", ft.icons.AUTORENEW, "#2196f3", lambda: None),
            menu_btn("Ayarlar", ft.icons.SETTINGS, "#757575", show_settings),
            ft.Divider(height=10),
            menu_btn("Çıxış", ft.icons.EXIT_TO_APP, "#d32f2f", lambda: page.window_destroy()),
        ], horizontal_alignment="center", spacing=15)
        
        page.add(top_bar, ft.Container(content=menu_col, padding=40, alignment=ft.alignment.center))
        update_top_bar()

    def menu_btn(text, icon, color, action):
        return ft.ElevatedButton(
            content=ft.Row([ft.Icon(icon, color="white"), ft.Text(text, size=18, weight="bold")], alignment="center"),
            style=ft.ButtonStyle(color="white", bgcolor=color, shape=ft.RoundedRectangleBorder(radius=15)),
            width=280, height=55, on_click=lambda _: action()
        )

    # --- 3. MƏNİM BAĞIM (Hay Day Stili Ferma) ---
    def show_farm():
        page.controls.clear()
        page.bgcolor = "#aed581"
        
        grid = ft.GridView(expand=True, runs_count=3, max_extent=110, spacing=10, run_spacing=10)
        for i in range(1, 10):
            is_unlocked = i <= state["unlocked_plots"]
            grid.controls.append(
                ft.Container(
                    content=ft.Icon(ft.icons.LOCK if not is_unlocked else ft.icons.LOCAL_FLORIST, color="white" if not is_unlocked else "pink"),
                    bgcolor="#8d6e63" if is_unlocked else "#5d4037",
                    border_radius=10, alignment=ft.alignment.center,
                    border=ft.border.all(2, "white30")
                )
            )

        back_btn = ft.IconButton(ft.icons.ARROW_BACK, icon_color="white", on_click=lambda _: show_main_menu())
        
        page.add(
            top_bar,
            ft.Row([back_btn, ft.Text("Mənim Bağım", size=24, weight="bold", color="white")], alignment="start"),
            ft.Container(content=grid, width=350, height=350, padding=20)
        )

    # --- 4. OYUN MEXANİKASI (Yeni Sözlər) ---
    def start_game():
        if state["lives"] <= 0:
            state["lives"] = 3 # Oyuna təzə girəndə 3 can hədiyyə!
        load_question()

    def load_question():
        page.controls.clear()
        page.bgcolor = "#f5f5f5"
        
        current_data = DATA[state["current_step"]]
        word_info = current_data[state["word_index"]]
        
        word_display = ft.Text(word_info["word"], size=45, weight="bold", color="#333333")
        step_info = ft.Text(f"Step {state['current_step']} - Sual {state['word_index']+1}/10", color="grey")
        
        options_col = ft.Column(spacing=15, horizontal_alignment="center")
        
        choices = word_info["options"].copy()
        random.shuffle(choices)
        
        for option in choices:
            btn = ft.ElevatedButton(
                text=option,
                width=280, height=60,
                style=ft.ButtonStyle(
                    color="black87", bgcolor="white",
                    shape=ft.RoundedRectangleBorder(radius=12),
                ),
                on_click=lambda e, opt=option, corr=word_info["correct"]: check_answer(opt, corr)
            )
            options_col.controls.append(btn)

        back_btn = ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: show_main_menu())

        page.add(
            top_bar,
            ft.Row([back_btn], alignment="start"),
            ft.Container(
                content=ft.Column([step_info, word_display, ft.Divider(height=40, color="transparent"), options_col], horizontal_alignment="center"),
                padding=20, alignment=ft.alignment.center, expand=True
            )
        )
        update_top_bar()

    # --- 5. CAVABIN YOXLANIŞI VƏ CAN SİSTEMİ ---
    def check_answer(selected, correct):
        if selected == correct:
            # DÜZGÜN CAVAB
            state["coins"] += 2
            state["exp"] += 1
            if state["exp"] >= 100:
                state["exp"] = 0
                state["level"] += 1
                page.snack_bar = ft.SnackBar(ft.Text("TƏBRİKLƏR! LEVEL UP! 🎉", color="white"), bgcolor="green")
                page.snack_bar.open = True
            
            state["word_index"] += 1
            
            # Step bitdimi? (10 sual)
            if state["word_index"] >= 10:
                state["word_index"] = 0
                state["current_step"] += 1
                state["unlocked_plots"] += 1 # Yeni torpaq açılır
                page.snack_bar = ft.SnackBar(ft.Text("Step Tamamlandı! Yeni Torpaq Açıldı! 🚜", color="white"), bgcolor="blue")
                page.snack_bar.open = True
                show_main_menu()
            else:
                load_question()
        else:
            # SƏHV CAVAB (Hardcore)
            state["lives"] -= 1
            if state["lives"] <= 0:
                show_death_popup() # Can bitdi, mağaza gəlir
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Səhv! 1 Can getdi 💔", color="white"), bgcolor="red")
                page.snack_bar.open = True
                update_top_bar()
                # Sualı dəyişmədən eyni sualda saxlayırıq ki, düzünü tapsın

    # --- 6. ÖLÜM EKRANI (Can Satışı) ---
    def show_death_popup():
        def buy_life(lives_to_buy, price):
            if state["coins"] >= price:
                state["coins"] -= price
                state["lives"] += lives_to_buy
                page.close(dlg)
                update_top_bar()
                load_question() # Qaldığı yerdən davam edir
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Pulun çatmır! 💰", color="white"), bgcolor="red")
                page.snack_bar.open = True
                page.update()

        def restart_step():
            state["lives"] = 3 # Yenidən 3 can veririk
            state["word_index"] = 0 # 1-ci suala qayıdırıq
            page.close(dlg)
            load_question()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Məğlub Oldun! 💔", color="red", weight="bold"),
            content=ft.Column([
                ft.Text("Qaldığın yerdən davam etmək üçün can al:"),
                ft.ElevatedButton("1 Can ❤️ - 10 💰", on_click=lambda _: buy_life(1, 10), bgcolor="green50"),
                ft.ElevatedButton("3 Can ❤️❤️❤️ - 25 💰", on_click=lambda _: buy_life(3, 25), bgcolor="blue50"),
                ft.ElevatedButton("5 Can ❤️❤️❤️❤️❤️ - 40 💰", on_click=lambda _: buy_life(5, 40), bgcolor="purple50"),
                ft.Divider(),
                ft.TextButton("İmtina et (Step-in əvvəlinə qayıt)", on_click=lambda _: restart_step(), style=ft.ButtonStyle(color="red"))
            ], tight=True, spacing=10),
        )
        page.open(dlg)

    # --- 7. AYARLAR MENYUSU ---
    def show_settings():
        dlg = ft.AlertDialog(
            title=ft.Text("Ayarlar"),
            content=ft.Column([
                ft.Switch(label="Səs", value=state["sound"], on_change=lambda e: state.update({"sound": e.control.value})),
                ft.Switch(label="Vibrasiya", value=state["vibration"], on_change=lambda e: state.update({"vibration": e.control.value})),
            ], tight=True),
            actions=[ft.TextButton("Bağla", on_click=lambda e: page.close(dlg))]
        )
        page.open(dlg)

    # OYUNU BAŞLAT
    asyncio.run(show_splash())

ft.app(target=main)
  

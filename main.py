import flet as ft
import asyncio
import random

# --- BÜTÜN FUNKSİYANI ASYNC EDİRİK ---
async def main(page: ft.Page):
    # --- SƏHİFƏ AYARLARI ---
    page.title = "Lingua Farm"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.bgcolor = "#f5f5f5"

    # --- OYUNUN YADDAŞI ---
    state = {
        "coins": 100,
        "lives": 3,
        "exp": 0,
        "level": 1,
        "current_step": 1,
        "word_index": 0,
        "unlocked_plots": 1,
        "sound": True,
        "vibration": True
    }

    # --- SÖZLƏR BAZASI (Tam 20 Step) ---
    DATA = {
        1: [
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
        ],
        2: [
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
        ],
        3: [
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
        4: [
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
        5: [
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
        6: [
            {"word": "HEAD", "correct": "baş", "options": ["baş", "əzələ", "sümük"]},
            {"word": "EYE", "correct": "göz", "options": ["göz", "qulaq", "burun"]},
            {"word": "EAR", "correct": "qulaq", "options": ["qulaq", "dil", "diş"]},
            {"word": "NOSE", "correct": "burun", "options": ["burun", "çənə", "alın"]},
            {"word": "MOUTH", "correct": "ağiz", "options": ["ağiz", "dodaq", "boğaz"]},
            {"word": "HAND", "correct": "əl", "options": ["əl", "barmaq", "bilək"]},
            {"word": "FOOT", "correct": "ayaq", "options": ["ayaq", "diz", "topuq"]},
            {"word": "HAIR", "correct": "saç", "options": ["saç", "qaş", "kirpik"]},
            {"word": "FACE", "correct": "üz", "options": ["üz", "boyun", "çiyin"]},
            {"word": "HEART", "correct": "ürək", "options": ["ürək", "ağciyər", "mədə"]}
        ],
        7: [
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
        8: [
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
        9: [
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
        10: [
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
        11: [
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
        12: [
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
        13: [
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
        14: [
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
        15: [
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
        16: [
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
        17: [
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
        18: [
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
        19: [
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
        20: [
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
        ]
    }

    # --- ÜST PANEL ---
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
        top_bar.content.controls

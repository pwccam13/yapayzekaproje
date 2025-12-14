import time
import os
import random

# [SUNUM NOTU]: Kütüphane bağımlılıklarını yönetiyoruz.
# Eğer 'requests' yoksa program çökmesin, 'Graceful Degradation' yaparak sadece TXT modunda çalışsın diye try-except bloğu kullandım.
try:
    import requests

    API_AKTIF = True
except ImportError:
    API_AKTIF = False
    print("[SİSTEM] 'requests' kütüphanesi eksik. Sadece Yerel Veri (TXT) modu aktif.")

# ==========================================
# KONFİGÜRASYON VE BİLGİ TABANI (KNOWLEDGE BASE)
# ==========================================

API_KEY = "RGAPI-d0caadfc-0fc3-4fc8-981d-f615ee1a9122"
REGION_GAME = "tr1"
REGION_ACCOUNT = "europe"

# 1. DETAYLI TERMİNOLOJİ SÖZLÜĞÜ (TÜM ROLLER İÇİN)
# [SUNUM NOTU]: False Positive eşleşmeleri önlemek için keyword'leri özelleştirdim.
# Örn: 'Skirmisher' hem AD hem AP olabildiği için, AD kategorisinde 'Critical' ve 'Duelist' gibi daha spesifik terimler kullandım.
GENEL_SINIFLAR = {
    # --- ÜST KORİDOR (TOP) ---
    "Tank & Ön Saf": ["Tank", "Warden", "Main: Ornn", "Main: Shen", "Main: Malphite", "Main: Sion", "Main: Cho'Gath", "Main: K'Sante"],
    "Ağır Dövüşçü (Juggernaut)": ["Juggernaut", "Darius", "Garen", "Sett", "Mordekaiser", "Urgot", "Illaoi", "Nasus", "Volibear"],
    "Ayrık İttiren (Splitpusher)": ["Splitpush", "Duelist", "Fiora", "Camille", "Jax", "Tryndamere", "Yorick", "Quinn"],
    "AP Dövüşçü / Menzilli": ["Main: Gwen", "Main: Rumble", "Main: Kennen", "Main: Teemo", "Main: Vladimir", "Main: Kayle"],

    # --- ORMAN (JUNGLE) ---
    "Erken Oyun & Baskıncı (Ganker)": ["Engage", "Diver", "Lee Sin", "Jarvan IV", "Elise", "Xin Zhao", "Rek'Sai", "Vi", "Nunu"],
    "Power Farm & Taşıyıcı": ["Carry", "Graves", "Kindred", "Lillia", "Nidalee", "Karthus", "Taliyah", "Bel'Veth", "Master Yi"],
    "Suikastçı Ormancı": ["Assassin", "Kha'Zix", "Rengar", "Evelynn", "Kayn", "Shaco", "Nocturne", "Ekko"],
    "Tank Ormancı": ["Tank", "Sejuani", "Zac", "Amumu", "Rammus", "Maokai"],

    # --- ORTA KORİDOR (MID) ---
    "Kontrol Büyücüsü (Control Mage)": ["Control", "Zone", "Orianna", "Syndra", "Anivia", "Azir", "Viktor", "Hwei", "Lissandra", "Malzahar"],
    "Suikastçı (Assassin)": ["Assassin", "Roam", "Zed", "Leblanc", "Akali", "Qiyana", "Talon", "Fizz", "Katarina", "Naafiri"],
    # DÜZELTME BURADA YAPILDI: 'Skirmisher' ve 'Fighter' kelimeleri çıkarıldı, yerine 'Critical' eklendi.
    "AD Skirmisher (Dövüşçü)": ["Critical", "Duelist", "Yasuo", "Yone", "Irelia", "Tristana", "Akshan", "Jayce", "Pantheon", "Renekton"],
    "Geç Oyun Büyücüsü (Scaling)": ["Scaling", "Late Game", "Kassadin", "Vladimir", "Veigar", "Aurelion Sol", "Ryze", "Kayle"],
    "Artillery (Menzilli Büyücü)": ["Artillery", "Poke", "Xerath", "Ziggs", "Vel'Koz", "Lux"],

    # --- NİŞANCI (ADC) ---
    "Hipertaşıyıcı (Hypercarry)": ["Hypercarry", "Scaling", "Jinx", "Vayne", "Kog'Maw", "Zeri", "Aphelios", "Twitch", "Smolder"],
    "Koridor Zorbası (Lane Bully)": ["Lane Bully", "Snowball", "Draven", "Lucian", "Kalista", "Caitlyn", "Miss Fortune", "Varus"],
    "Dive Lane (İçeri Giren)": ["Diver", "Mobile", "All-in", "Samira", "Kai'Sa", "Tristana", "Nilah"],
    "Fayda & Dürtme (Utility)": ["Utility", "Poke", "Ashe", "Jhin", "Ezreal", "Sivir", "Senna", "Ziggs"],

    # --- DESTEK (SUPPORT) ---
    "Efsuncu (Enchanter)": ["Enchanter", "Heal", "Shield", "Protect", "Lulu", "Janna", "Soraka", "Yuumi", "Nami", "Milio", "Karma"],
    "Başlatıcı Tank (Engage)": ["Engage", "Hook", "Nautilus", "Leona", "Thresh", "Blitzcrank", "Alistar", "Rell", "Rakan"],
    "Koruyucu (Warden)": ["Warden", "Disengage", "Braum", "Tahm Kench", "Taric"],
    "Mage Support (Hasar)": ["Mage", "Poke", "Lux", "Xerath", "Brand", "Zyra", "Vel'Koz", "Pyke"]
}
# [SUNUM NOTU]: Kullanıcı Deneyimini (UX) artırmak için Context-Aware (Bağlam Duyarlı) filtreleme yaptım.
# Yani kullanıcı ADC seçerse karşısına Tank seçenekleri çıkıp kafa karıştırmıyor.
ROL_FILTRESI = {
    "Ust Koridor": ["Tank & Ön Saf", "Ağır Dövüşçü (Juggernaut)", "Ayrık İttiren (Splitpusher)",
                    "AP Dövüşçü / Menzilli"],
    "Orman": ["Erken Oyun & Baskıncı (Ganker)", "Power Farm & Taşıyıcı", "Suikastçı Ormancı", "Tank Ormancı"],
    "Orta Koridor": ["Kontrol Büyücüsü (Control Mage)", "Suikastçı (Assassin)", "AD Skirmisher (Dövüşçü)",
                     "Geç Oyun Büyücüsü (Scaling)", "Artillery (Menzilli Büyücü)"],
    "Nisanci (ADC)": ["Hipertaşıyıcı (Hypercarry)", "Koridor Zorbası (Lane Bully)", "Dive Lane (İçeri Giren)",
                      "Fayda & Dürtme (Utility)"],
    "Destek": ["Efsuncu (Enchanter)", "Başlatıcı Tank (Engage)", "Koruyucu (Warden)", "Mage Support (Hasar)"]
}


# ==========================================
# 1. NESNE YÖNELİMLİ PROGRAMLAMA (OOP) YAPISI
# ==========================================

class Oyuncu:
    def __init__(self, ad, puan, rol, ozellik_str):
        self.ad = ad
        self.puan = puan
        self.rol = rol

        # [SUNUM NOTU]: Veri Normalizasyonu (Data Cleaning) yapıyorum.
        # Örneğin ADC rolünde 'Assassin' etiketi gelirse, bunu literatüre uygun olan 'Dive Lane' ile değiştiriyorum.
        # Bu sayede veriler daha tutarlı hale geliyor.
        if rol == "Nisanci (ADC)" and "Assassin" in ozellik_str:
            self.ozellik_str = ozellik_str.replace("Assassin", "Dive Lane")
        elif rol == "Orman" and "Hypercarry" in ozellik_str:
            self.ozellik_str = ozellik_str.replace("Hypercarry", "Carry")
        else:
            self.ozellik_str = ozellik_str

        self.ozellikler = [x.strip() for x in self.ozellik_str.replace('/', ',').split(',')]
        self.maas = puan * 10

    def __str__(self):
        return "{0} ({1}p) - {2}$".format(self.ad, self.puan, self.maas)


class Takim:
    # [SUNUM NOTU]: Takım bir 'Container Class'. Oyuncuları burada topluyor ve kümülatif (toplam) değerleri hesaplıyorum.
    def __init__(self):
        self.kadro = []
        self.toplam_maas = 0
        self.toplam_guc = 0

    def oyuncu_ekle(self, oyuncu):
        self.kadro.append(oyuncu)
        self.toplam_maas += oyuncu.maas
        self.toplam_guc += oyuncu.puan

    def rapor_ver(self):
        print("\n" + "=" * 80)
        print(f"[ TAKIM KADROSU - Ortalama Güç: {int(self.toplam_guc / 5)} ]")
        print("=" * 80)
        print("{:<15} {:<25} {:<6} {:<10} {}".format("ROL", "OYUNCU", "PUAN", "MAAS", "OZELLIK"))
        print("-" * 80)
        for oy in self.kadro:
            print("{:<15} {:<25} {:<6} {:<10} {}".format(oy.rol, oy.ad, oy.puan, f"{oy.maas}$", oy.ozellik_str))
        print("-" * 80)
        print(f"Toplam Maliyet: {self.toplam_maas}$")


# ==========================================
# 2. SİMÜLASYON MOTORU (KARŞILAŞTIRMA MANTIĞI)
# ==========================================

class StratejikMacMotoru:
    def __init__(self, oyuncu_havuzu):
        self.havuz = oyuncu_havuzu
        # [SUNUM NOTU]: Taş-Kağıt-Makas mantığına benzer bir 'Counter-Pick' sistemi kurdum.
        self.counter_tablosu = {
            "Assassin": ["Marksman", "Mage", "Support", "Sniper"],
            "Tank": ["Assassin", "Burst", "Mage"],
            "Marksman": ["Tank", "Juggernaut", "Fighter"],
            "Mage": ["Fighter", "Skirmisher"],
            "Fighter": ["Assassin", "Tank"],
            "Duelist": ["Tank", "Engage"]
        }

    def sinerji_hesapla(self, kadro):
        # [SUNUM NOTU]: Burası bir 'Heuristic Function' (Sezgisel Fonksiyon).
        # Takımın dengesine bakıp yapay bir puan (Reward/Penalty) üretiyor.
        tum_ozellikler = " ".join([o.ozellik_str for o in kadro])
        bonus = 0
        rapor = []

        # Kural 1: Tank yoksa ceza (-300)
        if any(x in tum_ozellikler for x in ["Tank", "Juggernaut", "Engage", "Warden"]):
            bonus += 250
            rapor.append("🛡️ TANK VAR (+250)")
        else:
            bonus -= 300
            rapor.append("⚠️ TANK EKSİK (-300)")

        # Kural 2: Hasar çeşitliliği varsa ödül (+200)
        has_ad = any(x in tum_ozellikler for x in
                     ["Marksman", "Fighter", "Assassin", "Duelist", "Lane Bully", "Hypercarry", "Skirmisher"])
        has_ap = any(x in tum_ozellikler for x in ["Mage", "Enchanter", "Control", "Magic", "Scaling"])

        if has_ad and has_ap:
            bonus += 200
            rapor.append("⚔️ HİBRİT HASAR (+200)")
        else:
            bonus -= 150
            rapor.append("⚠️ TEK TİP HASAR (-150)")

        return bonus, " | ".join(rapor)

    def rakip_olustur_gercek(self, benim_kadrom):
        # [SUNUM NOTU]: Random Sampling yöntemiyle havuzdan rastgele ama gerçek bir rakip takım oluşturuyoruz.
        rakip_kadro = []
        roller = ["Ust Koridor", "Orman", "Orta Koridor", "Nisanci (ADC)", "Destek"]
        benimkiler = [o.ad for o in benim_kadrom]

        for rol in roller:
            adaylar = [o for o in self.havuz if o.rol == rol and o.ad not in benimkiler]
            if adaylar:
                secilen = random.choice(adaylar)
                rakip_kadro.append(secilen)
            else:
                rakip_kadro.append(Oyuncu(f"Yedek {rol}", 800, rol, "Fighter"))
        return rakip_kadro

    def maci_hesapla(self, benim_takim):
        rakip_kadro = self.rakip_olustur_gercek(benim_takim.kadro)

        print("\n" + "#" * 60)
        print(" SİMÜLASYON BAŞLATILIYOR ".center(60, "#"))
        print("#" * 60)
        time.sleep(1)

        # Sinerji Analizi
        benim_sinerji, benim_rapor = self.sinerji_hesapla(benim_takim.kadro)
        rakip_sinerji, rakip_rapor = self.sinerji_hesapla(rakip_kadro)

        print(f"\n[TAKIM ANALİZİ]")
        print(f"SENİN TAKIM: {benim_rapor}")
        print(f">> Sinerji Etkisi: {benim_sinerji} Puan")
        print("-" * 40)
        print(f"RAKİP TAKIM: {rakip_rapor}")
        print(f">> Sinerji Etkisi: {rakip_sinerji} Puan")

        input("\nMaçı başlatmak için Enter'a bas...")

        skor_ben = 0
        skor_rakip = 0
        roller = ["Ust Koridor", "Orman", "Orta Koridor", "Nisanci (ADC)", "Destek"]

        print("\n--- KORİDOR EŞLEŞMELERİ ---")
        for i, rol in enumerate(roller):
            benim_oyuncu = benim_takim.kadro[i]
            rakip_oyuncu = rakip_kadro[i]

            # [SUNUM NOTU]: Normalizasyon: Takım sinerji puanını oyunculara eşit dağıtarak bireysel gücü güncelliyoruz.
            benim_guc = benim_oyuncu.puan + int(benim_sinerji / 5)
            rakip_guc = rakip_oyuncu.puan + int(rakip_sinerji / 5)

            ekstra_guc = 0
            avantaj_notu = ""

            # Counter-Pick hesaplaması
            for ozellik in benim_oyuncu.ozellikler:
                for anahtar, hedefler in self.counter_tablosu.items():
                    if anahtar in ozellik:
                        for rakip_ozellik in rakip_oyuncu.ozellikler:
                            if any(h in rakip_ozellik for h in hedefler):
                                ekstra_guc = 250
                                avantaj_notu = f" >> (KRİTİK AVANTAJ: {anahtar} vs {rakip_ozellik})"
                                break

            benim_toplam = benim_guc + ekstra_guc

            print(f"\n[{rol.upper()}]")
            print(f"   SEN  : {benim_oyuncu.ad} ({benim_guc}) {avantaj_notu}")
            print(f"   RAKİP: {rakip_oyuncu.ad} ({rakip_guc})")

            if ekstra_guc > 0: print(f"   STRATEJİ: +{ekstra_guc} Puan (Counter-Pick)")

            time.sleep(0.5)

            if benim_toplam >= rakip_guc:
                print(f"   ✅ KAZANAN: {benim_oyuncu.ad} (Fark: {benim_toplam - rakip_guc})")
                skor_ben += 1
            else:
                print(f"   ❌ KAYBEDEN: {benim_oyuncu.ad} (Eksik: {rakip_guc - benim_toplam})")
                skor_rakip += 1

        print("\n" + "=" * 60)
        print(f"MAÇ SONUCU: {skor_ben} - {skor_rakip}")
        if skor_ben > skor_rakip:
            print("🏆 TEBRİKLER! Stratejik üstünlükle kazandınız.")
        else:
            print("❌ MAĞLUBİYET. Takım kompozisyonu gözden geçirilmeli.")


# ==========================================
# 3. KARAR ALGORİTMASI (DECISION MAKING)
# ==========================================

class TransferYapayZekasi:
    def __init__(self, oyuncu_havuzu):
        self.havuz = oyuncu_havuzu

    def en_iyi_takimi_kur(self, butce, strateji):
        kurulan_takim = Takim()
        roller = ["Ust Koridor", "Orman", "Orta Koridor", "Nisanci (ADC)", "Destek"]
        print(f"\n[AI] Strateji: {strateji.upper()} | Havuz: {len(self.havuz)} Oyuncu taranıyor...")

        try:
            min_maas = min([oy.maas for oy in self.havuz])
        except:
            min_maas = 4000

        # [SUNUM NOTU]: Algoritma "Constraint Satisfaction" (Kısıt Sağlama) prensibiyle çalışır.
        # Bütçeyi aşmamak için gelecekteki turlar için rezerv ayırır (Dynamic Programming mantığına yakın).
        print(f"[AI] Bütçe Yönetimi: Her rol için minimum rezerv ({min_maas}$) ayrıldı.")

        # Ağırlıklandırma (Weighting): Seçilen stratejiye uygun oyunculara bonus puan verilir.
        bonus_kelimeler = []
        if strateji == "agresif":
            bonus_kelimeler = ["Assassin", "Fighter", "Marksman", "Duelist", "Snowball", "Lane Bully", "Ganker"]
        elif strateji == "scaling":
            bonus_kelimeler = ["Mage", "Tank", "Hypercarry", "Scaling", "Late Game", "Power Farm"]
        else:
            bonus_kelimeler = ["Control", "Tank", "Engage", "Utility", "Skirmisher"]

        takimda_tank_var = False

        # GREEDY (AÇGÖZLÜ) YAKLAŞIM: Her adımda o anki en iyi seçeneği alır.
        for i, rol in enumerate(roller):
            adaylar = [o for o in self.havuz if o.rol == rol]
            en_iyi_aday = None
            en_yuksek_skor = -99999

            kalan_rol_sayisi = 4 - i
            zorunlu_rezerv = kalan_rol_sayisi * min_maas

            # [SUNUM NOTU]: Burası kritik. Eğer takımda tank yoksa, algoritma stratejiyi görmezden gelip
            # zorla Tank seçmeye yönlendirilir (Heuristic Override).
            tank_lazim = False
            if not takimda_tank_var and rol in ["Ust Koridor", "Orman", "Destek"]:
                tank_lazim = True

            for aday in adaylar:
                # 1. Taban Puan
                skor = aday.puan

                # 2. Strateji Bonusu
                for ozellik in aday.ozellikler:
                    for bonus in bonus_kelimeler:
                        if bonus in ozellik:
                            skor += (aday.puan * 0.1)  # %10 Ağırlık artışı
                            break

                # 3. İhtiyaç Analizi
                is_tank = any(x in aday.ozellik_str for x in ["Tank", "Juggernaut", "Engage", "Warden"])

                if tank_lazim and is_tank:
                    skor += 500  # Tank seçimi için büyük teşvik (Bias)

                # Bütçe Kontrolü
                if (kurulan_takim.toplam_maas + aday.maas + zorunlu_rezerv) <= butce:
                    if skor > en_yuksek_skor:
                        en_yuksek_skor = skor
                        en_iyi_aday = aday

            if en_iyi_aday:
                kurulan_takim.oyuncu_ekle(en_iyi_aday)
                if any(x in en_iyi_aday.ozellik_str for x in ["Tank", "Juggernaut", "Engage", "Warden"]):
                    takimda_tank_var = True
                print(f"   [+] {rol}: {en_iyi_aday.ad} ({en_iyi_aday.puan}p)")
            else:
                print(f"   [-] {rol} için bütçe yetersiz!")

        return kurulan_takim

    def takimi_analiz_et(self, takim):
        print("\n[ KOMPOZİSYON ANALİZİ ]")
        tum_ozellikler = []
        for oy in takim.kadro: tum_ozellikler.extend(oy.ozellikler)

        hasar = ["Marksman", "Assassin", "Mage", "Duelist", "Carry", "Hypercarry", "Lane Bully", "Skirmisher"]
        tank = ["Tank", "Fighter", "Engage", "Juggernaut", "Warden"]

        d_skor = sum(1 for x in tum_ozellikler for k in hasar if k in x)
        t_skor = sum(1 for x in tum_ozellikler for k in tank if k in x)

        if t_skor < 1:
            print("[UYARI] Ön saf (Tank/Fighter) eksik. Takım kırılgan!")
        elif d_skor < 2:
            print("[UYARI] Hasar (Carry) eksik. Takım savaş uzarsa kaybeder.")
        else:
            print("[BAŞARILI] Dengeli takım kompozisyonu oluşturuldu.")


# ==========================================
# 4. VERİ YÖNETİMİ (DATA HANDLING)
# ==========================================

def txt_oku():
    dosya_adi = r"C:\Users\bemir\PyCharmMiscProject\.venv\sıralama.txt"
    if not os.path.exists(dosya_adi):
        dosya_adi = "sıralama.txt"
        if not os.path.exists(dosya_adi):
            print(f"[HATA] '{dosya_adi}' bulunamadı! Lütfen 'veri_duzelt_v2.py' dosyasını çalıştırın.");
            return []

    nesneler = []
    print(f"\n[SİSTEM] '{dosya_adi}' ayrıştırılıyor (Parsing)...")
    with open(dosya_adi, "r", encoding="utf-8") as f:
        for satir in f:
            if not satir.strip(): continue
            try:
                # CSV mantığıyla veriyi parçalayıp nesneleştiriyoruz.
                bilgi = satir.split(",")
                if len(bilgi) >= 4:
                    nesneler.append(Oyuncu(bilgi[0].strip(), int(bilgi[1]), bilgi[2].strip(), bilgi[3].strip()))
            except:
                continue
    print(f"[BAŞARILI] {len(nesneler)} oyuncu RAM'e yüklendi.")
    return nesneler


def sampiyon_verisi_getir():
    # [SUNUM NOTU]: Riot API'den JSON formatında güncel veriyi çekiyoruz.
    try:
        ver = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]
        data = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{ver}/data/tr_TR/champion.json").json()['data']
        champ_dict = {}
        for k, v in data.items():
            champ_dict[int(v['key'])] = (v['name'], v['tags'])
        return champ_dict
    except:
        return {}


def riot_api_cek(limit=300):
    if not API_AKTIF: return []
    print("\n[SİSTEM] Riot Games API bağlantısı kuruluyor...")
    headers = {"X-Riot-Token": API_KEY}
    oyuncu_listesi = []

    champ_data = sampiyon_verisi_getir()
    if not champ_data: print("[HATA] Şampiyon verisi alınamadı!"); return []

    try:
        url = f"https://{REGION_GAME}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5"
        resp = requests.get(url, headers=headers)
        entries = sorted(resp.json()['entries'], key=lambda x: x['leaguePoints'], reverse=True)[:limit]
    except:
        return []

    print(f"[SİSTEM] {len(entries)} oyuncu analiz ediliyor...")

    for i, p in enumerate(entries):
        lp = p['leaguePoints']
        puuid = p.get('puuid')
        ad = "Bilinmiyor";
        rol = "Belirsiz";
        ozellik = "Dengeli"

        # [SUNUM NOTU]: API Rate Limit (Hız Sınırı) aşmamak için yapay gecikme (Sleep) ekledim.
        time.sleep(1.2)
        print(f"\rİlerleme: %{(i + 1) * 100 // len(entries)}", end="")

        try:
            acc_resp = requests.get(
                f"https://{REGION_ACCOUNT}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}",
                headers=headers)
            if acc_resp.status_code == 200:
                d = acc_resp.json();
                ad = f"{d['gameName']}#{d['tagLine']}"

            mast_resp = requests.get(
                f"https://{REGION_GAME}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}",
                headers=headers)
            if mast_resp.status_code == 200:
                m = mast_resp.json()
                if m:
                    cid = m[0]['championId']
                    if cid in champ_data:
                        c_name, c_tags = champ_data[cid]
                        ozellik = " / ".join(c_tags)
                        if "Support" in c_tags:
                            rol = "Destek"
                        elif "Marksman" in c_tags:
                            rol = "Nisanci (ADC)"
                        elif "Mage" in c_tags:
                            rol = "Orta Koridor"
                        elif "Tank" in c_tags:
                            rol = "Ust Koridor"
                        elif "Assassin" in c_tags:
                            rol = "Orman"
                        else:
                            rol = "Ust Koridor"

                        if "Assassin" in c_tags and "Mage" not in c_tags: rol = "Orman"
        except:
            pass

        oyuncu_listesi.append(Oyuncu(ad, lp, rol, ozellik))

    print("\n[BAŞARILI] Veri çekme işlemi tamamlandı.")
    return oyuncu_listesi


# ==========================================
# 5. KULLANICI ARAYÜZÜ (UI)
# ==========================================

def rol_secimi():
    while True:
        print("\n--- SCOUTING (Oyuncu Arama) ---")
        print("[1] Ust Koridor")
        print("[2] Orman")
        print("[3] Orta Koridor")
        print("[4] Nisanci (ADC)")
        print("[5] Destek")
        print("[6] Geri Dön")

        secim = input("Secim: ").strip()
        rol_map = {"1": "Ust Koridor", "2": "Orman", "3": "Orta Koridor", "4": "Nisanci (ADC)", "5": "Destek"}

        if secim == "6":
            return
        elif secim in rol_map:
            ozellik_secimi(rol_map[secim])
        else:
            print("Hatali secim.")


def ozellik_secimi(rol):
    ilgili = [o for o in OYUNCU_HAVUZU if o.rol == rol]
    if not ilgili: print("Bu kriterde oyuncu verisi bulunamadı."); return

    print(f"\n--- {rol.upper()} - OYUNCU TİPİ SEÇİMİ ---")

    # [SUNUM NOTU]: Context-Aware Menü: Sadece o rol için anlamlı olan alt sınıfları gösterir.
    if rol in ROL_FILTRESI:
        kategoriler = ROL_FILTRESI[rol]
    else:
        kategoriler = list(GENEL_SINIFLAR.keys())

    for i, kat in enumerate(kategoriler, 1):
        print(f"[{i}] {kat}")

    print(f"[{len(kategoriler) + 1}] Tüm Oyuncuları Listele")
    print(f"[{len(kategoriler) + 2}] Geri")

    try:
        s = int(input("Secim: "))
        if s == len(kategoriler) + 2:
            return
        elif s == len(kategoriler) + 1:
            sonuclari_listele(rol, "Hepsi")
        elif 1 <= s <= len(kategoriler):
            secilen_kategori = kategoriler[s - 1]
            sonuclari_listele(rol, secilen_kategori)
        else:
            print("Hatalı seçim.")
    except:
        pass


def sonuclari_listele(rol, kategori_adi):
    print(f"\n[FİLTRE] {rol} | {kategori_adi}")
    eslesen = []

    for oy in OYUNCU_HAVUZU:
        if oy.rol != rol: continue

        if kategori_adi == "Hepsi":
            eslesen.append(oy)
        else:
            # Genel sınıflar sözlüğünden ilgili anahtar kelimeleri (Keyword Matching) bulur.
            aranan_kelimeler = GENEL_SINIFLAR.get(kategori_adi, [])
            if any(kelime in oy.ozellik_str for kelime in aranan_kelimeler):
                eslesen.append(oy)

    if not eslesen:
        print("Bu kriterlere uygun oyuncu bulunamadı.")
    else:
        eslesen.sort(key=lambda x: x.puan, reverse=True)
        print(f"\n[ BULUNAN: {len(eslesen)} OYUNCU ]")
        print("{:<20} {:<6} {:<10} {}".format("ISIM", "PUAN", "MAAS", "OZELLIK"))
        print("-" * 80)
        for oy in eslesen:
            maas_str = f"{oy.maas}$"
            print("{:<20} {:<6} {:<10} {}".format(oy.ad, oy.puan, maas_str, oy.ozellik_str))
        print("-" * 80)

    input("Devam etmek için Enter'a bas...")


def takim_kurma_modulu():
    print("\n--- TAKIM KURMA VE SİMÜLASYON ---")
    ai = TransferYapayZekasi(OYUNCU_HAVUZU)
    try:
        butce = int(input("Takım Bütçesi (Örn: 50000): "))
    except:
        return
    print("Oyun Stratejisi: [1] Agresif [2] Scaling (Geç Oyun) [3] Dengeli")
    s = input("Secim: ")
    st = "agresif" if s == "1" else ("scaling" if s == "2" else "dengeli")

    yeni = ai.en_iyi_takimi_kur(butce, st)
    if len(yeni.kadro) == 5:
        yeni.rapor_ver()
        ai.takimi_analiz_et(yeni)

        print("\nMaç simülasyonu başlatılsın mı? (e/h)")
        if input("Secim: ").lower() == 'e':
            StratejikMacMotoru(OYUNCU_HAVUZU).maci_hesapla(yeni)
    else:
        print("\n[HATA] Takım tamamlanamadı. Bütçe çok düşük olabilir.")


def main():
    global OYUNCU_HAVUZU
    print("\n##########################################")
    print(" ESPOR MENAJER ASISTANI (AKILLI SİSTEM)")
    print("##########################################")

    print("\nVeri Kaynağı Seçimi:")
    print("[1] Yerel Veri Tabanı (sıralama.txt)")
    print("[2] Canlı Sunucu (Riot Games API)")

    secim = input("Secim: ")

    if secim == "2":
        print("\nAnaliz edilecek oyuncu sayısı (Varsayılan: 300)")
        limit_giris = input("Sayı: ")
        try:
            limit = int(limit_giris)
        except ValueError:
            limit = 300
        OYUNCU_HAVUZU = riot_api_cek(limit)
    else:
        OYUNCU_HAVUZU = txt_oku()

    if not OYUNCU_HAVUZU: return

    while True:
        print("\n--- ANA MENU ---")
        print(f"[Veri Tabanı: {len(OYUNCU_HAVUZU)} Oyuncu]")
        print("[1] Yapay Zeka ile Takım Kur")
        print("[2] Oyuncu Analizi (Scouting)")
        print("[3] Çıkış")
        s = input("Secim: ")
        if s == "1":
            takim_kurma_modulu()
        elif s == "2":
            rol_secimi()
        elif s == "3":
            break


if __name__ == "__main__":
    main()

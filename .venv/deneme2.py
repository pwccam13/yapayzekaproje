import time
import os
import random
import sys
import concurrent.futures  # [YENİ] Multithreading kütüphanesi

# [SUNUM NOTU]: Kütüphane bağımlılıklarını yönetiyoruz.
try:
    import requests

    API_AKTIF = True
except ImportError:
    API_AKTIF = False
    print("[SİSTEM] 'requests' kütüphanesi eksik. Sadece Yerel Veri (TXT) modu aktif.")

# ==========================================
# KONFİGÜRASYON VE BİLGİ TABANI
# ==========================================

# [DİKKAT]: Sunumdan hemen önce Key'i yenile!
API_KEY = "RGAPI-9b85a10e-27cb-4ed8-9bb8-873cc7257e4b"
REGION_GAME = "tr1"
REGION_ACCOUNT = "europe"

# 1. DETAYLI TERMİNOLOJİ SÖZLÜĞÜ
GENEL_SINIFLAR = {
    "Tank & Ön Saf": ["Tank", "Warden", "Main: Ornn", "Main: Shen", "Main: Malphite", "Main: Sion", "Main: K'Sante"],
    "Ağır Dövüşçü (Juggernaut)": ["Juggernaut", "Darius", "Garen", "Sett", "Mordekaiser", "Urgot", "Illaoi",
                                  "Volibear"],
    "Ayrık İttiren (Splitpusher)": ["Splitpush", "Duelist", "Fiora", "Camille", "Jax", "Tryndamere", "Yorick", "Quinn"],
    "AP Dövüşçü / Menzilli": ["Main: Gwen", "Main: Rumble", "Main: Kennen", "Main: Teemo", "Main: Vladimir",
                              "Main: Kayle"],
    "Erken Oyun & Baskıncı (Ganker)": ["Engage", "Diver", "Lee Sin", "Jarvan IV", "Elise", "Xin Zhao", "Vi", "Nunu"],
    "Power Farm & Taşıyıcı": ["Carry", "Graves", "Kindred", "Lillia", "Nidalee", "Karthus", "Taliyah", "Master Yi"],
    "Suikastçı Ormancı": ["Assassin", "Kha'Zix", "Rengar", "Evelynn", "Kayn", "Shaco", "Nocturne", "Ekko"],
    "Tank Ormancı": ["Tank", "Sejuani", "Zac", "Amumu", "Rammus", "Maokai"],
    "Kontrol Büyücüsü (Control Mage)": ["Control", "Zone", "Orianna", "Syndra", "Anivia", "Azir", "Viktor", "Hwei",
                                        "Lissandra"],
    "Suikastçı (Assassin)": ["Assassin", "Roam", "Zed", "Leblanc", "Akali", "Qiyana", "Talon", "Fizz", "Katarina"],
    "AD Skirmisher (Dövüşçü)": ["Critical", "Duelist", "Yasuo", "Yone", "Irelia", "Tristana", "Akshan", "Jayce",
                                "Pantheon"],
    "Geç Oyun Büyücüsü (Scaling)": ["Scaling", "Late Game", "Kassadin", "Vladimir", "Veigar", "Aurelion Sol", "Ryze"],
    "Artillery (Menzilli Büyücü)": ["Artillery", "Poke", "Xerath", "Ziggs", "Vel'Koz", "Lux"],
    "Hipertaşıyıcı (Hypercarry)": ["Hypercarry", "Scaling", "Jinx", "Vayne", "Kog'Maw", "Zeri", "Aphelios", "Twitch"],
    "Koridor Zorbası (Lane Bully)": ["Lane Bully", "Snowball", "Draven", "Lucian", "Kalista", "Caitlyn",
                                     "Miss Fortune"],
    "Dive Lane (İçeri Giren)": ["Diver", "Mobile", "All-in", "Samira", "Kai'Sa", "Tristana", "Nilah"],
    "Fayda & Dürtme (Utility)": ["Utility", "Poke", "Ashe", "Jhin", "Ezreal", "Sivir", "Senna", "Ziggs"],
    "Efsuncu (Enchanter)": ["Enchanter", "Heal", "Shield", "Protect", "Lulu", "Janna", "Soraka", "Yuumi", "Nami",
                            "Karma"],
    "Başlatıcı Tank (Engage)": ["Engage", "Hook", "Nautilus", "Leona", "Thresh", "Blitzcrank", "Alistar", "Rell",
                                "Rakan"],
    "Koruyucu (Warden)": ["Warden", "Disengage", "Braum", "Tahm Kench", "Taric"],
    "Mage Support (Hasar)": ["Mage", "Poke", "Lux", "Xerath", "Brand", "Zyra", "Vel'Koz", "Pyke"]
}

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
# 1. TEMEL SINIFLAR (OOP)
# ==========================================

class Oyuncu:
    def __init__(self, ad, puan, rol, ozellik_str):
        self.ad = ad
        self.puan = puan
        self.rol = rol
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
# 2. MATCH ENGINE (SİMÜLASYON MOTORU)
# ==========================================

class StratejikMacMotoru:
    def __init__(self, oyuncu_havuzu):
        self.havuz = oyuncu_havuzu
        self.counter_tablosu = {
            "Assassin": ["Marksman", "Mage", "Support", "Sniper"],
            "Tank": ["Assassin", "Burst", "Mage"],
            "Marksman": ["Tank", "Juggernaut", "Fighter"],
            "Mage": ["Fighter", "Skirmisher"],
            "Fighter": ["Assassin", "Tank"],
            "Duelist": ["Tank", "Engage"]
        }

    def sinerji_hesapla(self, kadro):
        tum_ozellikler = " ".join([o.ozellik_str for o in kadro])
        bonus = 0
        rapor = []
        if any(x in tum_ozellikler for x in ["Tank", "Juggernaut", "Engage", "Warden"]):
            bonus += 250
            rapor.append("🛡️ TANK VAR (+250)")
        else:
            bonus -= 300
            rapor.append("⚠️ TANK EKSİK (-300)")
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
        rakip_kadro = []
        roller = ["Ust Koridor", "Orman", "Orta Koridor", "Nisanci (ADC)", "Destek"]
        benimkiler = [o.ad for o in benim_kadrom]
        for rol in roller:
            adaylar = [o for o in self.havuz if o.rol == rol and o.ad not in benimkiler]
            if adaylar:
                secilen = random.choice(adaylar)
                rakip_kadro.append(secilen)
            else:
                rakip_kadro.append(Oyuncu(f"Yedek {rol}", 1200, rol, "Fighter"))
        return rakip_kadro

    def maci_hesapla(self, benim_takim):
        rakip_kadro = self.rakip_olustur_gercek(benim_takim.kadro)
        print("\n" + "#" * 60)
        print(" SİMÜLASYON BAŞLATILIYOR ".center(60, "#"))
        print("#" * 60)
        time.sleep(1)
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
            benim_guc = benim_oyuncu.puan + int(benim_sinerji / 5)
            rakip_guc = rakip_oyuncu.puan + int(rakip_sinerji / 5)
            ekstra_guc_ben = 0
            ekstra_guc_rakip = 0
            avantaj_notu = ""

            for ozellik in benim_oyuncu.ozellikler:
                for anahtar, hedefler in self.counter_tablosu.items():
                    if anahtar in ozellik:
                        for rakip_ozellik in rakip_oyuncu.ozellikler:
                            if any(h in rakip_ozellik for h in hedefler):
                                ekstra_guc_ben = 250
                                avantaj_notu = f" >> (KRİTİK AVANTAJ: {anahtar} vs {rakip_ozellik})"
                                break
            for r_ozellik in rakip_oyuncu.ozellikler:
                for anahtar, hedefler in self.counter_tablosu.items():
                    if anahtar in r_ozellik:
                        for ozellik in benim_oyuncu.ozellikler:
                            if any(h in ozellik for h in hedefler):
                                ekstra_guc_rakip = 250
                                avantaj_notu += f" << (RAKİP AVANTAJI: {anahtar} vs {ozellik})"
                                break
            benim_toplam = benim_guc + ekstra_guc_ben
            rakip_toplam = rakip_guc + ekstra_guc_rakip
            print(f"\n[{rol.upper()}]")
            print(f"   SEN  : {benim_oyuncu.ad} ({benim_guc})")
            print(f"   RAKİP: {rakip_oyuncu.ad} ({rakip_guc})")
            print(f"   {avantaj_notu}")
            if ekstra_guc_ben > 0: print(f"   STRATEJİ: Senin Avantajın +{ekstra_guc_ben} Puan")
            if ekstra_guc_rakip > 0: print(f"   TEHLİKE:  Rakip Avantajı +{ekstra_guc_rakip} Puan")
            time.sleep(0.5)
            if benim_toplam >= rakip_toplam:
                print(f"   ✅ KAZANAN: {benim_oyuncu.ad} (Fark: {benim_toplam - rakip_toplam})")
                skor_ben += 1
            else:
                print(f"   ❌ KAYBEDEN: {benim_oyuncu.ad} (Eksik: {rakip_toplam - benim_toplam})")
                skor_rakip += 1
        print("\n" + "=" * 60)
        print(f"MAÇ SONUCU: {skor_ben} - {skor_rakip}")
        if skor_ben > skor_rakip:
            print("🏆 TEBRİKLER! Stratejik üstünlükle kazandınız.")
        else:
            print("❌ MAĞLUBİYET. Takım kompozisyonu gözden geçirilmeli.")


# ==========================================
# 3. KARAR ALGORİTMASI (AI - AKILLI BÜTÇE)
# ==========================================

class TransferYapayZekasi:
    def __init__(self, oyuncu_havuzu):
        self.havuz = oyuncu_havuzu

    def en_iyi_takimi_kur(self, butce, strateji):
        kurulan_takim = Takim()
        roller = ["Ust Koridor", "Orman", "Orta Koridor", "Nisanci (ADC)", "Destek"]

        try:
            min_maas = min([oy.maas for oy in self.havuz])
        except:
            min_maas = 4000

        bonus_kelimeler = []
        if strateji == "agresif":
            bonus_kelimeler = ["Assassin", "Fighter", "Marksman", "Duelist", "Snowball", "Lane Bully", "Ganker"]
        elif strateji == "scaling":
            bonus_kelimeler = ["Mage", "Tank", "Hypercarry", "Scaling", "Late Game", "Power Farm"]
        else:
            bonus_kelimeler = ["Control", "Tank", "Engage", "Utility", "Skirmisher"]

        takimda_tank_var = False

        # [ALGORİTMA NOTU]: Lookahead Optimization (İleriye Bakışlı Optimizasyon)
        for i, rol in enumerate(roller):
            adaylar = [o for o in self.havuz if o.rol == rol]
            en_iyi_aday = None
            en_yuksek_skor = -99999

            # Dinamik Rezerv: Kalan roller için minimum parayı ayırıyoruz.
            kalan_rol_sayisi = 4 - i
            rezerv_butce = kalan_rol_sayisi * min_maas
            harcanabilir_limit = butce - kurulan_takim.toplam_maas - rezerv_butce

            tank_lazim = False
            if not takimda_tank_var and rol in ["Ust Koridor", "Orman", "Destek"]:
                tank_lazim = True

            for aday in adaylar:
                if aday.maas > harcanabilir_limit: continue  # Bütçe Koruma

                skor = aday.puan
                for ozellik in aday.ozellikler:
                    for bonus in bonus_kelimeler:
                        if bonus in ozellik:
                            skor += (aday.puan * 0.1)
                            break

                is_tank = any(x in aday.ozellik_str for x in ["Tank", "Juggernaut", "Engage", "Warden"])
                if tank_lazim and is_tank: skor += 500

                if skor > en_yuksek_skor:
                    en_yuksek_skor = skor
                    en_iyi_aday = aday

            if en_iyi_aday:
                kurulan_takim.oyuncu_ekle(en_iyi_aday)
                if any(x in en_iyi_aday.ozellik_str for x in ["Tank", "Juggernaut", "Engage", "Warden"]):
                    takimda_tank_var = True

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
# 4. VERI YÖNETİMİ (MULTITHREADING & POOLING)
# ==========================================

def txt_oku():
    dosya_adi = "sıralama.txt"
    if not os.path.exists(dosya_adi):
        base_path = os.path.dirname(os.path.abspath(__file__))
        dosya_adi = os.path.join(base_path, "sıralama.txt")
    if not os.path.exists(dosya_adi):
        print(f"[HATA] '{dosya_adi}' bulunamadı!");
        return []
    nesneler = []
    print(f"\n[SİSTEM] '{dosya_adi}' ayrıştırılıyor (Parsing)...")
    with open(dosya_adi, "r", encoding="utf-8") as f:
        for satir in f:
            if not satir.strip(): continue
            try:
                bilgi = satir.split(",")
                if len(bilgi) >= 4:
                    nesneler.append(Oyuncu(bilgi[0].strip(), int(bilgi[1]), bilgi[2].strip(), bilgi[3].strip()))
            except:
                continue
    print(f"[BAŞARILI] {len(nesneler)} oyuncu RAM'e yüklendi.")
    return nesneler


def sampiyon_verisi_getir():
    try:
        ver = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]
        data = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{ver}/data/tr_TR/champion.json").json()['data']
        champ_dict = {}
        for k, v in data.items():
            champ_dict[int(v['key'])] = (v['name'], v['tags'])
        return champ_dict
    except:
        return {}


# [TEKNİK DETAY]: Bu fonksiyon "Thread" içinde çalışacak.
# Session nesnesi parametre olarak alınır (Connection Pooling).
def tekil_oyuncu_analiz(entry, session, headers, champ_data, yedek_roller):
    lp = entry['leaguePoints']
    puuid = entry.get('puuid')
    ad = f"Player_Unknown"
    rol = random.choice(yedek_roller)
    ozellik = "Dengeli"

    try:
        # 1. Hesap Bilgisi
        acc_resp = session.get(f"https://{REGION_ACCOUNT}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}",
                               headers=headers)
        if acc_resp.status_code == 200:
            d = acc_resp.json();
            ad = f"{d['gameName']}#{d['tagLine']}"

        # 2. Şampiyon Ustalığı
        mast_resp = session.get(
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

    return Oyuncu(ad, lp, rol, ozellik)


def riot_api_cek(limit=300):
    if not API_AKTIF: return []
    print("\n[SİSTEM] Riot Games API bağlantısı kuruluyor (Multithreaded)...")
    headers = {"X-Riot-Token": API_KEY}

    champ_data = sampiyon_verisi_getir()
    if not champ_data: print("[HATA] Şampiyon verisi alınamadı!"); return []

    try:
        url = f"https://{REGION_GAME}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5"
        resp = requests.get(url, headers=headers)
        entries = sorted(resp.json()['entries'], key=lambda x: x['leaguePoints'], reverse=True)[:limit]
    except Exception as e:
        print(f"[HATA] API Hatası: {e}");
        return []

    print(f"[SİSTEM] {len(entries)} oyuncu için {min(len(entries), 5)} thread başlatılıyor...")
    oyuncu_listesi = []
    yedek_roller = ["Ust Koridor", "Orman", "Orta Koridor", "Nisanci (ADC)", "Destek"]

    # [OPTIMIZASYON]: Session Pooling & Multithreading
    # 'requests.Session()' TCP bağlantısını açık tutar, hız kazandırır.
    # 'ThreadPoolExecutor' aynı anda birden fazla istek atar.
    with requests.Session() as session:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # Görevleri dağıt
            futures = [executor.submit(tekil_oyuncu_analiz, p, session, headers, champ_data, yedek_roller) for p in
                       entries]

            count = 0
            for future in concurrent.futures.as_completed(futures):
                oyuncu_listesi.append(future.result())
                count += 1
                # Thread-Safe Progress Bar
                yuzde = count * 100 // len(entries)
                bar = "█" * (yuzde // 5) + "-" * (20 - (yuzde // 5))
                sys.stdout.write(f"\r[{bar}] %{yuzde} Veri İndirildi")
                sys.stdout.flush()

    print("\n[BAŞARILI] Veri çekme ve işleme tamamlandı.")
    return oyuncu_listesi


# ==========================================
# 5. PERFORMANS ANALİZİ (BENCHMARK)
# ==========================================

def benchmark_testi(oyuncu_havuzu):
    print("\n" + "#" * 60)
    print(" MONTE CARLO SİMÜLASYONU (GÖRSEL MOD) ".center(60, "#"))
    print("#" * 60)

    döngü_sayisi = 10000
    print(f"[SİSTEM] {döngü_sayisi} Maçlık 'Stress Testi' başlatılıyor...")

    tp = 0;
    fp = 0;
    tn = 0;
    fn = 0
    ai = TransferYapayZekasi(oyuncu_havuzu)
    motor = StratejikMacMotoru(oyuncu_havuzu)

    # AKILLI ZORLUK AYARI
    if len(oyuncu_havuzu) < 100:
        ZORLUK_CARPANI = 1.15
        print("[AYAR] Dar Havuz (API) -> Zorluk: 1.15 (Dengeli)")
    else:
        ZORLUK_CARPANI = 1.45
        print("[AYAR] Geniş Havuz (TXT) -> Zorluk: 1.45 (Yüksek)")

    print("-" * 60)

    for i in range(döngü_sayisi):
        if i % 10 < 4:
            butce = random.randint(15000, 30000)
        else:
            butce = random.randint(40000, 80000)

        strateji = random.choice(["agresif", "scaling", "dengeli"])
        ai_takim = ai.en_iyi_takimi_kur(butce, strateji)
        if len(ai_takim.kadro) < 5: continue

        rakip_kadro = motor.rakip_olustur_gercek(ai_takim.kadro)

        # 1. TAHMİN
        ai_toplam_puan = sum(o.puan for o in ai_takim.kadro)
        rakip_toplam_puan = sum(o.puan for o in rakip_kadro)
        tahmin_kazanma = ai_toplam_puan > (rakip_toplam_puan * ZORLUK_CARPANI)

        # 2. GERÇEK SONUÇ
        ai_sinerji, _ = motor.sinerji_hesapla(ai_takim.kadro)
        rakip_sinerji, _ = motor.sinerji_hesapla(rakip_kadro)

        skor_ai = 0
        skor_rakip = 0

        for k in range(5):
            guc_ai = ai_takim.kadro[k].puan + int(ai_sinerji / 5)
            guc_rakip = rakip_kadro[k].puan + int(rakip_sinerji / 5)

            # Counter (Sen Rakibi?)
            for ozellik in ai_takim.kadro[k].ozellikler:
                for anahtar, hedefler in motor.counter_tablosu.items():
                    if anahtar in ozellik:
                        for r_ozellik in rakip_kadro[k].ozellikler:
                            if any(h in r_ozellik for h in hedefler):
                                guc_ai += 400;
                                break

            # Counter (Rakip Seni?)
            for r_ozellik in rakip_kadro[k].ozellikler:
                for anahtar, hedefler in motor.counter_tablosu.items():
                    if anahtar in r_ozellik:
                        for ozellik in ai_takim.kadro[k].ozellikler:
                            if any(h in ozellik for h in hedefler):
                                guc_rakip += 400;
                                break

            # Handikap & Kaos
            guc_rakip = guc_rakip * ZORLUK_CARPANI
            guc_ai = guc_ai * random.uniform(0.75, 1.25)
            guc_rakip = guc_rakip * random.uniform(0.75, 1.25)

            if guc_ai >= guc_rakip:
                skor_ai += 1
            else:
                skor_rakip += 1

        gercek_sonuc_kazanma = skor_ai > skor_rakip

        if tahmin_kazanma and gercek_sonuc_kazanma:
            tp += 1
        elif tahmin_kazanma and not gercek_sonuc_kazanma:
            fp += 1
        elif not tahmin_kazanma and not gercek_sonuc_kazanma:
            tn += 1
        elif not tahmin_kazanma and gercek_sonuc_kazanma:
            fn += 1

        # GÖRSEL ŞÖLEN (Progress Bar & Stats)
        yuzde = (i + 1) * 100 // döngü_sayisi
        bar_uzunluk = 30
        dolu = int(bar_uzunluk * (i + 1) / döngü_sayisi)
        bar = "█" * dolu + "-" * (bar_uzunluk - dolu)

        sys.stdout.write(f"\r[{bar}] %{yuzde} | TP:{tp} TN:{tn} (Doğru) | FP:{fp} FN:{fn} (Yanlış)")
        sys.stdout.flush()

    accuracy = (tp + tn) / ((tp + fp + tn + fn) or 1)
    precision = tp / ((tp + fp) or 1)
    recall = tp / ((tp + fn) or 1)
    f1_score = 2 * (precision * recall) / ((precision + recall) or 1)

    print("\n\n" + "=" * 60)
    print(" SONUÇ RAPORU (CONFUSION MATRIX) ")
    print("=" * 60)
    print(f"TP (Doğru Tahmin):    {tp}")
    print(f"FP (Yanlış Tahmin):   {fp}")
    print(f"TN (Doğru Negatif):   {tn}")
    print(f"FN (Sürpriz Sonuç):   {fn}")
    print("-" * 60)
    print(f"ACCURACY:  %{accuracy * 100:.2f}")
    print(f"PRECISION: %{precision * 100:.2f}")
    print(f"RECALL:    %{recall * 100:.2f}")
    print(f"F1 SCORE:  {f1_score:.3f}")
    print("=" * 60)
    input("Ana menüye dönmek için Enter'a bas...")


# ==========================================
# 6. UI & MAIN
# ==========================================

def rol_secimi():
    while True:
        print("\n--- SCOUTING ---")
        print("[1] Ust [2] Orman [3] Orta [4] ADC [5] Destek [6] Geri")
        secim = input("Secim: ").strip()
        rol_map = {"1": "Ust Koridor", "2": "Orman", "3": "Orta Koridor", "4": "Nisanci (ADC)", "5": "Destek"}
        if secim == "6":
            return
        elif secim in rol_map:
            ozellik_secimi(rol_map[secim])


def ozellik_secimi(rol):
    ilgili = [o for o in OYUNCU_HAVUZU if o.rol == rol]
    if not ilgili: print("Oyuncu yok."); return
    print(f"\n--- {rol} ---")
    if rol in ROL_FILTRESI:
        kategoriler = ROL_FILTRESI[rol]
    else:
        kategoriler = list(GENEL_SINIFLAR.keys())
    for i, kat in enumerate(kategoriler, 1): print(f"[{i}] {kat}")
    print(f"[{len(kategoriler) + 1}] Hepsi\n[{len(kategoriler) + 2}] Geri")
    try:
        s = int(input("Secim: "))
        if s == len(kategoriler) + 2:
            return
        elif s == len(kategoriler) + 1:
            sonuclari_listele(rol, "Hepsi")
        elif 1 <= s <= len(kategoriler):
            sonuclari_listele(rol, kategoriler[s - 1])
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
            aranan = GENEL_SINIFLAR.get(kategori_adi, [])
            if any(k in oy.ozellik_str for k in aranan): eslesen.append(oy)
    if not eslesen:
        print("Yok.")
    else:
        eslesen.sort(key=lambda x: x.puan, reverse=True)
        print(f"\n[ BULUNAN: {len(eslesen)} ]")
        print("{:<20} {:<6} {:<10} {}".format("ISIM", "PUAN", "MAAS", "OZELLIK"))
        print("-" * 80)
        for oy in eslesen:
            print("{:<20} {:<6} {:<10} {}".format(oy.ad, oy.puan, f"{oy.maas}$", oy.ozellik_str))
        print("-" * 80)
    input("Devam...")


def takim_kurma_modulu():
    print("\n--- TAKIM KURMA ---")
    ai = TransferYapayZekasi(OYUNCU_HAVUZU)
    while True:
        giris = input("Bütçe (Örn: 50000): ").strip()
        if giris.isdigit():
            butce = int(giris);
            break
        else:
            print("Sayı giriniz!")
    print("Strateji: [1] Agresif [2] Scaling [3] Dengeli")
    s = input("Secim: ")
    st = "agresif" if s == "1" else ("scaling" if s == "2" else "dengeli")
    yeni = ai.en_iyi_takimi_kur(butce, st)
    if len(yeni.kadro) == 5:
        yeni.rapor_ver()
        ai.takimi_analiz_et(yeni)
        if input("\nSimülasyon? (e/h): ").lower() == 'e':
            StratejikMacMotoru(OYUNCU_HAVUZU).maci_hesapla(yeni)
    else:
        print("Bütçe yetersiz.")


def main():
    global OYUNCU_HAVUZU
    print("\n##########################################")
    print(" ESPOR MENAJER ASISTANI (AKILLI SİSTEM)")
    print("##########################################")
    print("[1] Yerel Veri (TXT)\n[2] Canlı Veri (API)")
    secim = input("Secim: ")
    if secim == "2":
        try:
            limit = int(input("Kişi Sayısı (örn: 50): "))
        except:
            limit = 50
        OYUNCU_HAVUZU = riot_api_cek(limit)
    else:
        OYUNCU_HAVUZU = txt_oku()
    if not OYUNCU_HAVUZU: return
    while True:
        print("\n--- ANA MENU ---")
        print(f"[Havuz: {len(OYUNCU_HAVUZU)}]")
        print("[1] Yapay Zeka Takım\n[2] Scouting\n[3] Performans Testi\n[4] Çıkış")
        s = input("Secim: ")
        if s == "1":
            takim_kurma_modulu()
        elif s == "2":
            rol_secimi()
        elif s == "3":
            benchmark_testi(OYUNCU_HAVUZU)
        elif s == "4":
            break


if __name__ == "__main__":
    main()

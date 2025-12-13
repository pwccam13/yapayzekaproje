import requests
import time
import sys

# --- AYARLAR ---
API_KEY = "RGAPI-f0029b54-5287-47b5-950a-3cbedd106ff9"  # Kendi Key'ini buraya yapıştır
REGION_GAME = "tr1"  # Oyun verisi (TR)
REGION_ACCOUNT = "europe"  # İsim verisi (Europe)
OUTPUT_FILE = "lol_sirilama.txt"  # Kaydedilecek dosya adı

# Hedef Oyuncu Sayısı
TARGET_COUNT = 500


def get_headers():
    return {"X-Riot-Token": API_KEY}


def get_champion_name_dict():
    """Şampiyon ID'lerini isme çevirmek için sözlük oluşturur."""
    try:
        ver = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]
        data = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{ver}/data/tr_TR/champion.json").json()['data']
        id_map = {}
        for k, v in data.items():
            id_map[int(v['key'])] = v['name']
        return id_map
    except:
        return {}


def get_top_players_list():
    """Challenger ve Grandmaster liglerini çekip birleştirir ve sıralar."""
    print("1/3 - Challenger listesi çekiliyor...")
    url_chal = f"https://{REGION_GAME}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5"
    resp_chal = requests.get(url_chal, headers=get_headers())

    if resp_chal.status_code != 200:
        print(f"Hata! Challenger çekilemedi. Kod: {resp_chal.status_code}")
        return []

    print("2/3 - Grandmaster listesi çekiliyor...")
    url_gm = f"https://{REGION_GAME}.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5"
    resp_gm = requests.get(url_gm, headers=get_headers())

    chal_entries = resp_chal.json().get('entries', [])
    gm_entries = []

    if resp_gm.status_code == 200:
        gm_entries = resp_gm.json().get('entries', [])

    # İki listeyi birleştir
    all_entries = chal_entries + gm_entries

    print(f"3/3 - Toplam {len(all_entries)} oyuncu bulundu. Puana göre sıralanıyor...")

    # Puana (LP) göre çoktan aza sırala
    sorted_players = sorted(all_entries, key=lambda x: x.get('leaguePoints', 0), reverse=True)

    # Sadece ilk 500 kişiyi döndür
    return sorted_players[:TARGET_COUNT]


def get_player_details(puuid):
    """Tek bir oyuncu için İsim ve Main Şampiyon sorgular."""
    headers = get_headers()

    # 1. İsim Sorgusu (Account V1)
    riot_id = "Bilinmiyor"
    try:
        acc_url = f"https://{REGION_ACCOUNT}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}"
        acc_resp = requests.get(acc_url, headers=headers)
        if acc_resp.status_code == 200:
            d = acc_resp.json()
            riot_id = f"{d.get('gameName')}#{d.get('tagLine')}"
        elif acc_resp.status_code == 429:
            print("\n!!! HIZ LİMİTİNE TAKILDIK - BEKLENİYOR !!!")
            time.sleep(10)
    except:
        pass

    # 2. Main Şampiyon Sorgusu (Mastery V4)
    champ_id = 0
    try:
        mast_url = f"https://{REGION_GAME}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}"
        mast_resp = requests.get(mast_url, headers=headers)
        if mast_resp.status_code == 200:
            m_data = mast_resp.json()
            if m_data:
                champ_id = m_data[0]['championId']
        elif mast_resp.status_code == 429:
            print("\n!!! HIZ LİMİTİNE TAKILDIK - BEKLENİYOR !!!")
            time.sleep(10)
    except:
        pass

    return riot_id, champ_id


def save_to_file(text, mode="a"):
    """Metni dosyaya kaydeder. Varsayılan mod: ekleme (append)."""
    try:
        with open(OUTPUT_FILE, mode, encoding="utf-8") as f:
            f.write(text + "\n")
    except Exception as e:
        print(f"Dosya hatası: {e}")


def main():
    print(f"\n{'=' * 60}")
    print(f"TR SUNUCUSU İLK {TARGET_COUNT} OYUNCU SIRALAMASI BAŞLATILIYOR")
    print("UYARI: Riot Dev Key limitleri sebebiyle bu işlem")
    print("yaklaşık 20-25 dakika sürecektir.")
    print(f"Veriler '{OUTPUT_FILE}' dosyasına anlık olarak yazılacaktır.")
    print(f"{'=' * 60}\n")

    # 1. Şampiyon İsimlerini Al
    champ_dict = get_champion_name_dict()

    # 2. Listeyi Hazırla (Challenger + GM)
    target_players = get_top_players_list()

    if not target_players:
        print("Liste oluşturulamadı. Program sonlanıyor.")
        return

    # Dosyayı sıfırla ve başlıkları yaz
    header = f"{'Sıra':<5} | {'Oyuncu Adı':<30} | {'LP':<6} | {'Main Şampiyon'}"
    seperator = "-" * 75

    print(header)
    print(seperator)

    # Dosyayı "w" (write) moduyla açıp sıfırlıyoruz
    save_to_file(header, mode="w")
    save_to_file(seperator, mode="a")

    # 3. Döngüye Gir ve Verileri Çek
    for i, player in enumerate(target_players):
        rank = i + 1
        lp = player.get('leaguePoints', 0)
        puuid = player.get('puuid')

        # Detayları çek
        name, c_id = get_player_details(puuid)
        c_name = champ_dict.get(c_id, "Bilinmiyor")

        # Satırı formatla
        row_str = f"{rank:<5} | {name:<30} | {lp:<6} | {c_name}"

        # 1. Ekrana Yazdır
        print(row_str)

        # 2. Dosyaya Kaydet (Append modu)
        save_to_file(row_str, mode="a")

        # --- KRİTİK NOKTA: RATE LIMIT ---
        time.sleep(2.5)

    print(f"\n{'=' * 60}")
    print(f"İŞLEM TAMAMLANDI! Sonuçlar '{OUTPUT_FILE}' dosyasına kaydedildi.")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
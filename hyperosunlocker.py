"""
HyperOS Bootloader Unlocker - CLI Version
Copyright © 2026 SerdarOnline
https://forum.miuiturkiye.net/uyeler/serdaronline.99036/
MiuiTürkiye Forum: https://forum.miuiturkiye.net/

Bu yazılım SerdarOnline tarafından geliştirilmiştir.
Telif hakkı koruması altındadır.
"""

import hashlib
import random
import time
import json
import sys
import os
import re
import base64
import threading
from datetime import datetime, timedelta, timezone
import ntplib
import pytz
import urllib3

# ═══════════════════════════════════════════════════════════════════
# 🔒 LİSANS KORUMA SİSTEMİ - By SerdarOnline
# Bu kod SerdarOnline tarafından geliştirilmiştir.
# Telif hakkı koruması aktiftir. Yetkisiz değişiklik yasaktır.
# ═══════════════════════════════════════════════════════════════════

_LICENSE_SIGNATURE = "Q0hBUkFDVEVSaXplZEJ5U2VyZGFyT25saW5l"  # Base64: "CHARACTERizedBySerdarOnline"
_AUTHOR_HASH = "db4d3b2745ec26c7dde4fc0896a35a22"  # MD5 of "By SerdarOnline"
_INTEGRITY_KEY = "U2VyZGFyT25saW5l"  # Base64: "SerdarOnline"

def _verify_license():
    """Lisans doğrulama - Bu fonksiyon silinirse program çalışmaz"""
    try:
        # Signature kontrolü
        decoded = base64.b64decode(_LICENSE_SIGNATURE).decode('utf-8')
        if "SerdarOnline" not in decoded:
            return False
        
        # Author hash kontrolü  
        author_text = "By SerdarOnline"
        calculated_hash = hashlib.md5(author_text.encode('utf-8')).hexdigest()
        if calculated_hash != _AUTHOR_HASH:
            return False
        
        # Integrity key kontrolü
        integrity = base64.b64decode(_INTEGRITY_KEY).decode('utf-8')
        if integrity != "SerdarOnline":
            return False
            
        return True
    except:
        return False

def _check_author_integrity():
    """Yazar bilgisi kontrol - By SerdarOnline"""
    if not _verify_license():
        print("\n⚠️ LİSANS DOĞRULAMA HATASI\n")
        print("Bu yazılım SerdarOnline tarafından geliştirilmiştir.")
        print("Telif hakkı koruması ihlal edilmiştir.\n")
        print("Yetkisiz değişiklik tespit edildi.")
        print("Program sonlandırılıyor.\n")
        print("© 2026 SerdarOnline - Tüm hakları saklıdır.")
        sys.exit(1)

# Lisans kontrolü yap
_check_author_integrity()

# Log dosyası hazırlığı
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file_path = os.path.join(log_dir, f"hyperosunlocker_cli_{timestamp}.log")

# Log dosyasına başlangıç bilgisi yaz
with open(log_file_path, 'w', encoding='utf-8') as f:
    f.write("="*60 + "\n")
    f.write("HyperOS Bootloader Unlocker - CLI Version Log\n")
    f.write(f"Başlangıç: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("Copyright © 2026 SerdarOnline\n")
    f.write("="*60 + "\n\n")

# Renk kodları (colorama olmadan)
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def log_print(message, color="", end="\n"):
    """Hem terminale hem log dosyasına yazdır - By SerdarOnline"""
    # Terminale renkli yazdır
    print(color + message + Colors.ENDC, end=end)
    
    # Log dosyasına renksiz yazdır
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            # ANSI kodlarını temizle
            clean_message = re.sub(r'\033\[[0-9;]+m', '', message)
            timestamp_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp_now}] {clean_message}{end}")
    except Exception:
        pass  # Log yazma hatası olursa sessizce devam et

log_print(Colors.CYAN + Colors.BOLD + """
╔══════════════════════════════════════════════════════════════╗
║   HyperOS Bootloader Unlocker - CLI Version                 ║
║   Copyright © 2026 SerdarOnline                             ║
║   MiuiTürkiye Forum                                          ║
╚══════════════════════════════════════════════════════════════╝
""" + Colors.ENDC)
log_print(f"📁 Loglar kaydediliyor: {os.path.basename(log_file_path)}", Colors.CYAN)

# --- AYARLAR ---
TOKEN = "BURAYA_TOKEN_GELECEK"  # Yakaladığın token
USER_ID = "6167633761"          # Senin User ID'n
THREAD_COUNT = 10               # Aynı anda kaç istek gönderilsin?
FEEDTIME_MS = 450               # 19:00'dan kaç milisaniye önce başlasın? (Ping'e göre ayarla)
FAILOVER_ATTEMPTS = 2           # Her istek için kaç deneme yapılsın
REQUEST_TIMEOUT = 2.0           # İstek timeout süresi (saniye)

# URL - Sadece SGP endpoint çalışıyor
UNLOCK_URL = "https://sgp-api.buy.mi.com/bbs/api/global/apply/bl-auth"
CHECK_URL = "https://sgp-api.buy.mi.com/bbs/api/global/user/bl-switch/state"

# User-Agent çeşitleri (rotasyon için)
USER_AGENTS = [
    "okhttp/4.12.0",
    "okhttp/4.11.0",
    "okhttp/4.10.0",
    "Dalvik/2.1.0 (Linux; U; Android 13; MI 9 Build/TKQ1.220829.002)",
    "Dalvik/2.1.0 (Linux; U; Android 12; Redmi Note 11 Pro Build/SKQ1.211006.001)",
    "Dalvik/2.1.0 (Linux; U; Android 14; Xiaomi 13 Build/UKQ1.230804.001)",
]

def generate_device_id():
    return hashlib.sha1(f"{random.random()}{time.time()}".encode()).hexdigest().upper()

DEVICE_ID = generate_device_id()

# Bağlantı Havuzu
http = urllib3.PoolManager(
    maxsize=THREAD_COUNT + 5,
    timeout=urllib3.Timeout(connect=REQUEST_TIMEOUT, read=5.0),
    retries=False # Kota savaşında beklemeye vaktimiz yok, hata alırsak hemen yeni istek
)

def send_request(thread_id, start_beijing, start_ts, attempt=0):
    """Saldırı anında çalışan ana fonksiyon - By SerdarOnline"""
    # Dynamic User-Agent rotasyonu
    user_agent = USER_AGENTS[thread_id % len(USER_AGENTS)]
    
    headers = {
        "Cookie": f"new_bbs_serviceToken={TOKEN};userId={USER_ID};versionCode=500411;versionName=5.4.11;deviceId={DEVICE_ID};",
        "User-Agent": user_agent,
        "Content-Type": "application/json; charset=utf-8"
    }
    body = json.dumps({"is_retry": True}).encode('utf-8')
    
    now = datetime.now(timezone.utc).astimezone(pytz.timezone("Asia/Shanghai"))
    log_print(f"[Thread-{thread_id}] Başvuru gönderiliyor... Saat: {now.strftime('%H:%M:%S.%f')}", Colors.CYAN)
    
    try:
        resp = http.request('POST', UNLOCK_URL, headers=headers, body=body)
        
        # Server Date header'ını göster
        server_date = resp.headers.get('Date', 'Bilinmiyor')
        log_print(f"[Thread-{thread_id}] Server Date: {server_date}", Colors.BLUE)
        
        data = json.loads(resp.data.decode('utf-8'))
        code = data.get("code")
        
        if code == 0:
            res = data.get("data", {}).get("apply_result")
            if res == 1:
                log_print("!!! BAŞARILI !!! Kilit açma izni alındı.", Colors.GREEN + Colors.BOLD)
                return True
            elif res == 3:
                log_print(f"[Thread-{thread_id}] Kota dolmuş (Quota Reached).", Colors.RED)
        elif code in [500, 502, 503, 429]:
            # Rate limit veya server hatası - retry
            if attempt < FAILOVER_ATTEMPTS:
                log_print(f"[Thread-{thread_id}] Server hatası ({code}), yeniden deniyor... ({attempt+1}/{FAILOVER_ATTEMPTS})", Colors.YELLOW)
                time.sleep(0.05)  # 50ms bekle
                return send_request(thread_id, start_beijing, start_ts, attempt + 1)
            else:
                log_print(f"[Thread-{thread_id}] Maksimum deneme sayısına ulaşıldı.", Colors.RED)
        else:
            log_print(f"[Thread-{thread_id}] Sunucu Yanıtı: {data}", Colors.YELLOW)
    except Exception as e:
        if attempt < FAILOVER_ATTEMPTS:
            log_print(f"[Thread-{thread_id}] Hata: {e}, yeniden deniyor...", Colors.YELLOW)
            time.sleep(0.05)
            return send_request(thread_id, start_beijing, start_ts, attempt + 1)
        else:
            log_print(f"[Thread-{thread_id}] Hata: {e}", Colors.RED)
    
    return False

def attack_sequence(start_beijing, start_ts):
    """Zamanı gelince thread'leri ateşler"""
    threads = []
    success = False
    
    for i in range(THREAD_COUNT):
        t = threading.Thread(target=lambda tid: send_request(tid, start_beijing, start_ts), args=(i,))
        threads.append(t)
        t.start()
        # Staggered start: Her thread'i 5ms arayla başlat
        time.sleep(0.005)
    
    for t in threads:
        t.join()
    
    if success:
        log_print("\n✅ İşlem başarıyla tamamlandı!", Colors.GREEN + Colors.BOLD)
    else:
        log_print("\n⚠️ Tüm denemeler tamamlandı.", Colors.YELLOW)

def main():
    global TOKEN, USER_ID
    
    # Lisans kontrolü
    _check_author_integrity()
    
    log_print("Token ve User ID kontrol ediliyor...", Colors.CYAN)
    
    # TOKEN manuel girilmemişse interaktif olarak sor
    if TOKEN == "BURAYA_TOKEN_GELECEK":
        log_print("\n⚠️ TOKEN ayarlanmamış!", Colors.YELLOW)
        log_print("\nSeçenekler:", Colors.CYAN)
        log_print("  1. TOKEN'ı şimdi gir (interaktif)")
        log_print("  2. GUI versiyonunu kullan (önerilen)")
        log_print("  3. Çıkış")
        
        choice = input(Colors.BOLD + "\nSeçiminiz (1/2/3): " + Colors.ENDC).strip()
        
        if choice == "1":
            log_print("\n📝 TOKEN ve User ID girişi:", Colors.CYAN)
            TOKEN = input("  Token (new_bbs_serviceToken): ").strip()
            USER_ID = input("  User ID (userId): ").strip()
            
            if not TOKEN or not USER_ID:
                log_print("❌ TOKEN ve User ID boş bırakılamaz!", Colors.RED)
                sys.exit(1)
            
            log_print("✅ TOKEN başarıyla ayarlandı.", Colors.GREEN)
        elif choice == "2":
            log_print("\n💡 GUI versiyonunu başlatmak için:", Colors.CYAN)
            log_print("   python hyperosunlocker_gui.py", Colors.GREEN)
            sys.exit(0)
        else:
            log_print("\nProgram sonlandırıldı.", Colors.YELLOW)
            sys.exit(0)
    
    # 1. Saat Senkronizasyonu
    log_print("\n⏰ Zaman senkronize ediliyor...", Colors.YELLOW)
    client = ntplib.NTPClient()
    try:
        response = client.request('pool.ntp.org', version=3)
        ntp_now = datetime.fromtimestamp(response.tx_time, timezone.utc)
        beijing_tz = pytz.timezone("Asia/Shanghai")
        start_beijing = ntp_now.astimezone(beijing_tz)
        start_ts = time.time()
        log_print(f"✅ Pekin Saati: {start_beijing.strftime('%H:%M:%S')}", Colors.GREEN)
    except Exception as e:
        log_print(f"❌ NTP Hatası: {e}", Colors.RED)
        log_print("İnternetinizi kontrol edin veya farklı bir NTP sunucusu deneyin.", Colors.YELLOW)
        return

    # 2. Ping testi
    log_print("\n🌐 Endpoint ping testi yapılıyor...", Colors.CYAN)
    try:
        start_time = time.time()
        resp = http.request('HEAD', UNLOCK_URL, timeout=2.0)
        ping_ms = (time.time() - start_time) * 1000
        log_print(f"✅ SGP API Ping: {ping_ms:.0f}ms", Colors.GREEN)
        
        if ping_ms > 200:
            log_print(f"⚠️ Yüksek ping! FEEDTIME_MS değerini artırmayı düşünün (şu an: {FEEDTIME_MS}ms)", Colors.YELLOW)
    except Exception as e:
        log_print(f"⚠️ Ping testi başarısız: {e}", Colors.RED)

    # 3. Bekleme Modu
    target_time = (start_beijing + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    # Target time'dan FEEDTIME_MS kadar önce tetikle
    trigger_time = target_time - timedelta(milliseconds=FEEDTIME_MS)
    
    log_print(f"\n🎯 Hedef Saat: {target_time.strftime('%H:%M:%S')}", Colors.BLUE)
    log_print(f"⚡ Tetiklenme: {trigger_time.strftime('%H:%M:%S.%f')[:-3]}", Colors.BLUE)
    log_print("\n⏳ Bekleniyor, lütfen scripti kapatmayın...\n", Colors.YELLOW)

    while True:
        elapsed = time.time() - start_ts
        current_beijing = start_beijing + timedelta(seconds=elapsed)
        
        if current_beijing >= trigger_time:
            log_print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", Colors.BOLD + Colors.RED)
            log_print("        🚀 SALDIRI BAŞLADI 🚀", Colors.BOLD + Colors.RED)
            log_print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n", Colors.BOLD + Colors.RED)
            attack_sequence(start_beijing, start_ts)
            break
        
        # CPU'yu yormadan ama hassas kontrol
        time.sleep(0.001)
    
    log_print("\n" + "="*60, Colors.CYAN)
    log_print("Program sonlandırıldı - By SerdarOnline", Colors.BOLD)
    log_print("="*60, Colors.CYAN)
    
    # Log dosyasına sonlandırma bilgisi
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write("\n" + "="*60 + "\n")
            f.write(f"Program Sonlandırıldı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*60 + "\n")
    except:
        pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log_print("\n\n⚠️ Kullanıcı tarafından durduruldu.", Colors.YELLOW)
        log_print("Program sonlandırıldı - By SerdarOnline", Colors.CYAN)
        # Log dosyasına sonlandırma bilgisi
        try:
            with open(log_file_path, 'a', encoding='utf-8') as f:
                f.write("\n" + "="*60 + "\n")
                f.write(f"Program Durduruldu (Ctrl+C): {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*60 + "\n")
        except:
            pass
        sys.exit(0)
    except Exception as e:
        log_print(f"\n❌ Beklenmeyen hata: {e}", Colors.RED)
        # Log dosyasına hata bilgisi
        try:
            with open(log_file_path, 'a', encoding='utf-8') as f:
                f.write("\n" + "="*60 + "\n")
                f.write(f"HATA: {e}\n")
                f.write(f"Program Hata ile Sonlandırıldı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*60 + "\n")
        except:
            pass
        sys.exit(1)

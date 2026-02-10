import hashlib
import random
import time
import json
import sys
import os
import re
import ctypes
import threading
from datetime import datetime, timedelta, timezone
import ntplib
import pytz
import urllib3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTextEdit, QProgressBar, QGroupBox, QSpinBox,
                             QMessageBox, QFrame, QSystemTrayIcon, QMenu, QAction, QCheckBox, QDialog, QSplashScreen)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon, QPixmap, QDesktopServices
from PyQt5.QtCore import QUrl

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
    import base64
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
        msg = (
            "⚠️ LİSANS DOĞRULAMA HATASI\n\n"
            "Bu yazılım SerdarOnline tarafından geliştirilmiştir.\n"
            "Telif hakkı koruması ihlal edilmiştir.\n\n"
            "Yetkisiz değişiklik tespit edildi.\n"
            "Program sonlandırılıyor.\n\n"
            "© 2026 SerdarOnline - Tüm hakları saklıdır."
        )
        ctypes.windll.user32.MessageBoxW(0, msg, "Lisans Hatası - By SerdarOnline", 0x10)
        sys.exit(1)

class TokenFetcherThread(QThread):
    """Selenium ile token ve user ID çeken thread - By SerdarOnline"""
    log_signal = pyqtSignal(str, str)
    success_signal = pyqtSignal(str, str)  # token, user_id
    error_signal = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        _check_author_integrity()  # Lisans kontrolü
    
    def run(self):
        try:
            self.log_signal.emit("🌐 Tarayıcı açılıyor...", "info")
            
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), 
                options=options
            )
            
            driver.get("https://new.c.mi.com/global/")
            self.log_signal.emit("✅ Tarayıcı açıldı. Lütfen giriş yapın...", "warning")
            self.log_signal.emit("⏳ Token ve User ID bekleniyor...", "info")
            
            # Token ve User ID'yi bekle
            token = None
            user_id = None
            max_wait = 300  # 5 dakika maksimum bekleme
            wait_count = 0
            
            while (not token or not user_id) and wait_count < max_wait:
                try:
                    cookies = driver.get_cookies()
                    for cookie in cookies:
                        if cookie['name'] == 'new_bbs_serviceToken':
                            token = cookie['value']
                        elif cookie['name'] == 'userId':
                            user_id = cookie['value']
                    
                    # Eğer userId cookie'sinde yoksa, JavaScript ile almayı dene
                    if token and not user_id:
                        try:
                            # Local storage'dan userId'yi almayı dene
                            user_id = driver.execute_script(
                                "return document.cookie.match(/userId=([^;]+)/)?.[1] || "
                                "localStorage.getItem('userId') || "
                                "sessionStorage.getItem('userId')"
                            )
                        except:
                            pass
                    
                    if token and user_id:
                        self.log_signal.emit(f"✅ Token bulundu: {token[:30]}...", "success")
                        self.log_signal.emit(f"✅ User ID bulundu: {user_id}", "success")
                        break
                        
                except Exception as e:
                    pass
                    
                time.sleep(2)
                wait_count += 2
            
            driver.quit()
            
            if token and user_id:
                self.success_signal.emit(token, user_id)
            else:
                error_msg = "Token veya User ID bulunamadı. Lütfen düzgün giriş yaptığınızdan emin olun."
                self.log_signal.emit(f"❌ {error_msg}", "error")
                self.error_signal.emit(error_msg)
                
        except Exception as e:
            error_msg = f"Tarayıcı hatası: {str(e)}"
            self.log_signal.emit(f"❌ {error_msg}", "error")
            self.error_signal.emit(error_msg)


class WorkerThread(QThread):
    """Arka planda çalışan işçi thread - By SerdarOnline"""
    log_signal = pyqtSignal(str, str)  # mesaj, renk
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(bool, str)  # başarı durumu, mesaj
    
    def __init__(self, token, user_id, thread_count, feedtime_ms, test_mode=False, advanced_settings=None):
        super().__init__()
        _check_author_integrity()  # Lisans kontrolü
        self.token = token
        self.user_id = user_id
        self.thread_count = thread_count
        self.feedtime_ms = feedtime_ms
        self.test_mode = test_mode
        self.is_running = True
        self.device_id = hashlib.sha1(f"{random.random()}{time.time()}".encode()).hexdigest().upper()
        
        # Gelişmiş ayarları al veya varsayılan değerleri kullan
        if advanced_settings is None:
            advanced_settings = {
                'failover_attempts': 2,
                'staggered_delay_ms': 5,
                'request_timeout': 2.0,
                'dns_prefetch': True,
                'regions': {'sgp': True, 'hyperos': True, 'ru': True, 'fra': True, 'in': True, 'us': True}
            }
        self.advanced_settings = advanced_settings
        
        self.UNLOCK_URL = "https://sgp-api.buy.mi.com/bbs/api/global/apply/bl-auth"
        self.CHECK_URL = "https://sgp-api.buy.mi.com/bbs/api/global/user/bl-switch/state"
        
        # Dinamik User-Agent ve cihaz çeşitlendirmesi
        self.user_agents = [
            "Mozilla/5.0 (Linux; Android 14; Xiaomi 14 Pro) XiaomiCommunity/5.4.11",
            "Mozilla/5.0 (Linux; Android 13; Redmi Note 12 Pro) XiaomiCommunity/5.4.11",
            "Mozilla/5.0 (Linux; Android 14; Poco X6 Pro) XiaomiCommunity/5.4.11",
            "Mozilla/5.0 (Linux; Android 13; Mi 13 Ultra) XiaomiCommunity/5.4.11",
            "okhttp/4.12.0",
            "okhttp/4.11.0"
        ]
        
        # HTTP Pool Manager'i timeout ayarıyla oluştur
        timeout_val = self.advanced_settings.get('request_timeout', 2.0)
        self.http = urllib3.PoolManager(
            maxsize=self.thread_count + 5,
            timeout=urllib3.Timeout(connect=timeout_val, read=timeout_val + 3),
            retries=False
        )
        
    def stop(self):
        self.is_running = False
    
    def measure_ping(self):
        """Ping ölçümü yap"""
        try:
            start = time.time()
            self.http.request('HEAD', self.UNLOCK_URL, timeout=2.0)
            ping_ms = (time.time() - start) * 1000
            return ping_ms
        except Exception as e:
            self.log_signal.emit(f"⚠️ Ping ölçümü başarısız: {e}", "warning")
            return None
        
    def send_request(self, thread_id, target_url, attempt=0):
        """Hata durumunda diğer bölgelere otomatik zıplayan istek mekanizması"""
        max_attempts = self.advanced_settings.get('failover_attempts', 2)
        if not self.is_running or attempt > max_attempts:
            return
        
        # Failover endpoint listesi (sadece çalışan ve doğrulanmış endpoint'ler)
        endpoints = [
            "https://sgp-api.buy.mi.com/bbs/api/global/apply/bl-auth",
            "https://sgp-api.buy.mi.com/bbs/api/global/apply/bl-auth",
            "https://sgp-api.buy.mi.com/bbs/api/global/apply/bl-auth"
        ]
        
        # Dinamik User-Agent seçimi (thread_id'ye göre değişir)
        user_agent = self.user_agents[thread_id % len(self.user_agents)]
        
        headers = {
            "Cookie": f"new_bbs_serviceToken={self.token};userId={self.user_id};versionCode=500411;versionName=5.4.11;deviceId={self.device_id};",
            "User-Agent": user_agent,
            "Content-Type": "application/json; charset=utf-8",
            "Connection": "keep-alive"
        }
        body = json.dumps({"is_retry": True}).encode('utf-8')
        
        try:
            timeout_val = self.advanced_settings.get('request_timeout', 2.0)
            resp = self.http.request('POST', target_url, headers=headers, body=body, timeout=timeout_val)
            data = json.loads(resp.data.decode('utf-8'))
            code = data.get("code")
            
            # DURUM 1: BAŞARI VEYA KOTA BİTMESİ (İstek ulaştı demektir)
            if code == 0 or code == 100004:
                server_date = resp.headers.get('Date', 'Bilinmiyor')
                region = target_url.split('/')[2].split('.')[0]  # sgp-api, admin.m gibi
                self.log_signal.emit(f"[T-{thread_id}] 🎯 Sunucu Yanıtladı ({region}): Kod {code} | Saat: {server_date}", "info")
                
                if code == 0:
                    res = data.get("data", {}).get("apply_result")
                    if res == 1:
                        self.log_signal.emit("🎉 BAŞARILI! Kilit açma izni alındı!", "success")
                        self.finished_signal.emit(True, "Bootloader kilit açma izni başarıyla alındı!")
                    elif res == 3:
                        self.log_signal.emit("⚠️ Kota dolmuş (Quota Reached)", "warning")
                elif code == 100004:
                    self.log_signal.emit(f"⚠️ [T-{thread_id}] Kota bitti (Kod: 100004)", "warning")
                return
            
            # DURUM 2: SUNUCU YOĞUN VEYA HATA VERDİ (Failover tetikle)
            elif code in [500, 502, 503, 429] or resp.status != 200:
                try:
                    next_index = (endpoints.index(target_url) + 1) % len(endpoints)
                    next_url = endpoints[next_index]
                except ValueError:
                    # Eğer target_url listede yoksa ilk endpoint'i kullan
                    next_url = endpoints[0]
                
                self.log_signal.emit(f"🔄 [T-{thread_id}] {target_url.split('/')[2]} Hatalı (Kod: {code})! Yedek sunucuya geçiliyor...", "warning")
                time.sleep(0.05)  # 50ms bekle ve diğer sunucuya zıpla
                return self.send_request(thread_id, next_url, attempt + 1)
            
            else:
                # Bilinmeyen kod, logla ve devam et
                self.log_signal.emit(f"[T-{thread_id}] Sunucu Yanıtı: {data}", "warning")
        
        except Exception as e:
            # Bağlantı zaman aşımı veya ağ hatası olursa diğerine geç
            try:
                next_index = (endpoints.index(target_url) + 1) % len(endpoints)
                next_url = endpoints[next_index]
            except ValueError:
                next_url = endpoints[0]
            
            self.log_signal.emit(f"📡 [T-{thread_id}] Bağlantı koptu ({str(e)[:30]}...), yedek sunucuya geçiliyor...", "warning")
            return self.send_request(thread_id, next_url, attempt + 1)
    
    def attack_sequence(self):
        """Tüm thread'leri başlat"""
        self.log_signal.emit("\n🚀 === GLOBAL ÇOKLU BÖLGE SALDIRISI BAŞLATILDI === 🚀", "success")
        
        # Kullanıcı tarafından seçilen bölgeleri kullan
        # NOT: Test sonuçlarına göre sadece sgp-api çalışıyor
        all_endpoints = {
            'sgp': "https://sgp-api.buy.mi.com/bbs/api/global/apply/bl-auth",      # ⭐⭐⭐ SADECE BU ÇALIŞIYOR!
        }
        
        # Seçilen bölgeleri filtrele
        regions_config = self.advanced_settings.get('regions', {})
        endpoints = [url for key, url in all_endpoints.items() if regions_config.get(key, True)]
        
        # Eğer hiçbir bölge seçilmemişse varsayılan olarak hepsini kullan
        if not endpoints:
            endpoints = list(all_endpoints.values())
            self.log_signal.emit("⚠️ Hiç bölge seçilmemiş, tüm bölgeler kullanılıyor", "warning")
        
        self.log_signal.emit(f"🌍 Kullanılacak bölge sayısı: {len(endpoints)}", "info")
        
        # Staggered delay ayarını al
        staggered_delay = self.advanced_settings.get('staggered_delay_ms', 5) / 1000.0  # ms'den saniyeye çevir
        
        threads = []
        for i in range(self.thread_count):
            if not self.is_running:
                break
            
            # İstekleri mevcut tüm bölgeler arasında dengeli dağıt (Round Robin)
            target_url = endpoints[i % len(endpoints)]
            
            t = threading.Thread(target=self.send_request, args=(i, target_url))
            threads.append(t)
            t.start()
            
            # 🔥 STAGGERED START: Her thread arasına ayarlanmış gecikme koy
            if staggered_delay > 0:
                time.sleep(staggered_delay)
            self.progress_signal.emit(int((i + 1) / self.thread_count * 100))
        
        for t in threads:
            t.join()
            
    def run(self):
        """Ana işlem"""
        try:
            # TEST MODU - Direkt istek gönder
            if self.test_mode:
                self.log_signal.emit("🧪 TEST MODU - Direkt istek gönderiliyor...", "warning")
                self.attack_sequence()
                self.finished_signal.emit(True, "Test tamamlandı")
                return
            
            # 0. DNS Prefetching (Tüm endpoint'lere boş ping atarak DNS ön belleğe alınır)
            self.log_signal.emit("🌐 DNS ön belleğe alınıyor...", "info")
            dns_endpoints = [
                "https://unlock.update.miui.com",
                "https://global.unlock.update.miui.com",
                "https://sgp-api.buy.mi.com"
            ]
            for endpoint in dns_endpoints:
                try:
                    self.http.request('HEAD', endpoint, retries=0, timeout=1.0)
                except:
                    pass  # DNS çözümü yapıldı, hata önemsiz
            self.log_signal.emit("✅ DNS önbelleği hazır (3 ana sunucu)", "success")
            
            # 1. NTP Senkronizasyonu
            self.log_signal.emit("⏰ Zaman senkronize ediliyor...", "info")
            client = ntplib.NTPClient()
            
            try:
                response = client.request('pool.ntp.org', version=3)
                ntp_now = datetime.fromtimestamp(response.tx_time, timezone.utc)
                beijing_tz = pytz.timezone("Asia/Shanghai")
                start_beijing = ntp_now.astimezone(beijing_tz)
                start_ts = time.time()
                self.log_signal.emit(f"✅ Pekin Saati: {start_beijing.strftime('%Y-%m-%d %H:%M:%S')}", "success")
            except Exception as e:
                self.log_signal.emit(f"❌ NTP Hatası: {e}", "error")
                self.finished_signal.emit(False, "Zaman senkronizasyonu başarısız!")
                return
            
            # 2. Hedef zaman hesaplama
            target_time = (start_beijing + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            trigger_time = target_time - timedelta(milliseconds=self.feedtime_ms)
            
            self.log_signal.emit(f"🎯 Hedef Saat: {target_time.strftime('%H:%M:%S')}", "info")
            self.log_signal.emit(f"🚀 Tetiklenme: {trigger_time.strftime('%H:%M:%S.%f')}", "info")
            self.log_signal.emit("⏳ Bekleniyor...", "info")
            
            # 3. Bekleme döngüsü
            ping_checked = False
            warmed = False
            
            while self.is_running:
                elapsed = time.time() - start_ts
                current_beijing = start_beijing + timedelta(seconds=elapsed)
                
                # Progress bar güncelleme
                time_until_trigger = (trigger_time - current_beijing).total_seconds()
                if time_until_trigger > 0 and time_until_trigger < 3600:  # 1 saat içindeyse
                    progress = int((3600 - time_until_trigger) / 3600 * 100)
                    self.progress_signal.emit(progress)
                
                # Ping ölçümü (10 saniye öncesinde)
                if 9.5 < time_until_trigger < 10.0 and not ping_checked:
                    ping_ms = self.measure_ping()
                    if ping_ms:
                        self.log_signal.emit(f"📡 Ping: {ping_ms:.2f} ms", "info")
                    ping_checked = True
                
                # Connection pre-warming (2 saniye öncesinde)
                if 1.5 < time_until_trigger < 2.0 and not warmed:
                    self.log_signal.emit("🔥 Bağlantı ısıtılıyor...", "info")
                    threading.Thread(target=lambda: self.http.request('GET', "https://sgp-api.buy.mi.com/generate_204")).start()
                    warmed = True
                
                if current_beijing >= trigger_time:
                    self.attack_sequence()
                    break
                
                time.sleep(0.001)
                
        except Exception as e:
            self.log_signal.emit(f"❌ Kritik Hata: {e}", "error")
            self.finished_signal.emit(False, str(e))


class AdvancedSettingsDialog(QDialog):
    """Gelişmiş ayarlar popup penceresi - By SerdarOnline"""
    def __init__(self, parent=None, current_settings=None):
        super().__init__(parent)
        _check_author_integrity()  # Lisans kontrolü
        self.setWindowTitle("🔧 Gelişmiş Ayarlar - By SerdarOnline")
        self.setModal(True)
        self.setMinimumWidth(600)
        
        # Dark theme uygula
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #1a1c2e, stop:1 #2d3250);
            }
            QLabel {
                color: #e8e8e8;
            }
            QSpinBox, QCheckBox {
                color: #e8e8e8;
            }
            QPushButton {
                padding: 10px 20px;
                border: 2px solid #3d4463;
                border-radius: 8px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #3a7bd5, stop:1 #00d2ff);
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #2a6bc5, stop:1 #00c2ef);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #1a5bb5, stop:1 #00b2df);
            }
        """)
        
        # Mevcut ayarları yükle veya varsayılanları kullan
        if current_settings is None:
            current_settings = {
                'failover_attempts': 2,
                'staggered_delay_ms': 5,
                'request_timeout': 2.0,
                'dns_prefetch': True,
                'regions': {'sgp': True}
            }
        
        self.init_ui(current_settings)
    
    def init_ui(self, settings):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Başlık
        title = QLabel("⚙️ Gelişmiş Ayarlar")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #00d2ff; padding: 10px;")
        layout.addWidget(title)
        
        # Failover Denemesi
        failover_layout = QHBoxLayout()
        failover_label = QLabel("Failover Denemesi:")
        failover_label.setMinimumWidth(150)
        failover_label.setToolTip("Bir sunucu hata verdiğinde kaç farklı bölge denenir")
        self.failover_spin = QSpinBox()
        self.failover_spin.setMinimum(1)
        self.failover_spin.setMaximum(5)
        self.failover_spin.setValue(settings.get('failover_attempts', 2))
        self.failover_spin.setSuffix(" deneme")
        failover_layout.addWidget(failover_label)
        failover_layout.addWidget(self.failover_spin)
        failover_layout.addStretch()
        layout.addLayout(failover_layout)
        
        # Thread Başlatma Gecikmesi (Staggered Start)
        stagger_layout = QHBoxLayout()
        stagger_label = QLabel("Thread Aralığı:")
        stagger_label.setMinimumWidth(150)
        stagger_label.setToolTip("Her thread arasındaki gecikme (ms)")
        self.stagger_spin = QSpinBox()
        self.stagger_spin.setMinimum(0)
        self.stagger_spin.setMaximum(50)
        self.stagger_spin.setValue(settings.get('staggered_delay_ms', 5))
        self.stagger_spin.setSuffix(" ms")
        stagger_layout.addWidget(stagger_label)
        stagger_layout.addWidget(self.stagger_spin)
        stagger_layout.addStretch()
        layout.addLayout(stagger_layout)
        
        # İstek Timeout
        timeout_layout = QHBoxLayout()
        timeout_label = QLabel("İstek Timeout:")
        timeout_label.setMinimumWidth(150)
        timeout_label.setToolTip("HTTP istekleri için maksimum bekleme süresi")
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setMinimum(1)
        self.timeout_spin.setMaximum(10)
        self.timeout_spin.setValue(int(settings.get('request_timeout', 2.0)))
        self.timeout_spin.setSuffix(" saniye")
        timeout_layout.addWidget(timeout_label)
        timeout_layout.addWidget(self.timeout_spin)
        timeout_layout.addStretch()
        layout.addLayout(timeout_layout)
        
        # DNS Prefetch
        dns_layout = QHBoxLayout()
        self.dns_checkbox = QCheckBox("🌐 DNS Ön Belleğe Alma")
        self.dns_checkbox.setChecked(settings.get('dns_prefetch', True))
        self.dns_checkbox.setToolTip("Program başlamadan önce tüm bölgelerin DNS'ünü çöz")
        dns_layout.addWidget(self.dns_checkbox)
        dns_layout.addStretch()
        layout.addLayout(dns_layout)
        
        # Bölge Seçimi
        region_label = QLabel("🌍 Kullanılacak Bölgeler:")
        region_label.setStyleSheet("font-weight: bold; margin-top: 10px; color: #00d2ff;")
        layout.addWidget(region_label)
        
        regions = settings.get('regions', {})
        
        # İlk satır: Sadece çalışan endpoint
        regions_layout1 = QHBoxLayout()
        self.region_sgp = QCheckBox("🇸🇬 Singapur API (SADECE BU ÇALIŞIYOR)")
        self.region_sgp.setChecked(regions.get('sgp', True))
        self.region_sgp.setEnabled(False)  # Devre dışı bırak, diğerleri çalışmıyor
        self.region_sgp.setToolTip("sgp-api.buy.mi.com - Test edildi, çalışıyor")
        
        info_label = QLabel("⚠️ Diğer endpoint'ler şu anda çalışmıyor")
        info_label.setStyleSheet("color: #ffc107; font-size: 11px;")
        
        regions_layout1.addWidget(self.region_sgp)
        regions_layout1.addWidget(info_label)
        regions_layout1.addStretch()
        layout.addLayout(regions_layout1)
        
        # Butonlar
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.ok_button = QPushButton("✅ Tamam")
        self.ok_button.setMinimumWidth(120)
        self.ok_button.setMinimumHeight(35)
        self.ok_button.clicked.connect(self.accept)
        
        self.cancel_button = QPushButton("❌ İptal")
        self.cancel_button.setMinimumWidth(120)
        self.cancel_button.setMinimumHeight(35)
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
    
    def get_settings(self):
        """Dialog'dan ayarları al"""
        return {
            'failover_attempts': self.failover_spin.value(),
            'staggered_delay_ms': self.stagger_spin.value(),
            'request_timeout': float(self.timeout_spin.value()),
            'dns_prefetch': self.dns_checkbox.isChecked(),
            'regions': {
                'sgp': True  # Sadece bu çalışıyor
            }
        }


class HyperOSUnlockerGUI(QMainWindow):
    """Ana pencere sınıfı - Copyright © 2026 SerdarOnline"""
    def __init__(self):
        super().__init__()
        _check_author_integrity()  # Lisans kontrolü
        self.worker = None
        
        # Log dosyası için hazırlık
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
        os.makedirs(log_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file_path = os.path.join(log_dir, f"hyperosunlocker_{timestamp}.log")
        
        # Log dosyasına başlangıç bilgisi yaz
        with open(self.log_file_path, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("HyperOS Bootloader Unlocker - Log Dosyası\n")
            f.write(f"Başlangıç: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("Copyright © 2026 SerdarOnline\n")
            f.write("="*60 + "\n\n")
        
        # Gelişmiş ayarlar için varsayılan değerler
        self.advanced_settings = {
            'failover_attempts': 2,
            'staggered_delay_ms': 5,
            'request_timeout': 2.0,
            'dns_prefetch': True,
            'regions': {
                'sgp': True,  # Sadece bu endpoint çalışıyor
            }
        }
        
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("🔓 HyperOS Bootloader Unlocker - By SerdarOnline")
        self.setGeometry(100, 100, 900, 700)
        self.setStyleSheet(self.get_stylesheet())
        
        # Ana widget ve layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Başlık
        title_label = QLabel("🔓 HyperOS Bootloader Unlocker")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Ayarlar Paneli
        settings_group = QGroupBox("⚙️ Ayarlar")
        settings_group.setObjectName("groupBox")
        settings_layout = QVBoxLayout()
        
        # Otomatik Token Al Butonu
        auto_token_layout = QHBoxLayout()
        self.auto_token_button = QPushButton("🔑 Otomatik Token ve User ID Al")
        self.auto_token_button.setObjectName("autoTokenButton")
        self.auto_token_button.setMinimumHeight(40)
        self.auto_token_button.clicked.connect(self.fetch_token_automatically)
        auto_token_layout.addWidget(self.auto_token_button)
        settings_layout.addLayout(auto_token_layout)
        
        # Token girişi
        token_layout = QHBoxLayout()
        token_label = QLabel("Token:")
        token_label.setMinimumWidth(100)
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("new_bbs_serviceToken değerini buraya yapıştırın")
        token_layout.addWidget(token_label)
        token_layout.addWidget(self.token_input)
        settings_layout.addLayout(token_layout)
        
        # User ID girişi
        userid_layout = QHBoxLayout()
        userid_label = QLabel("User ID:")
        userid_label.setMinimumWidth(100)
        self.userid_input = QLineEdit()
        self.userid_input.setPlaceholderText("Kullanıcı ID'niz")
        userid_layout.addWidget(userid_label)
        userid_layout.addWidget(self.userid_input)
        settings_layout.addLayout(userid_layout)
        
        # Thread Count
        thread_layout = QHBoxLayout()
        thread_label = QLabel("Thread Sayısı:")
        thread_label.setMinimumWidth(100)
        self.thread_spin = QSpinBox()
        self.thread_spin.setMinimum(1)
        self.thread_spin.setMaximum(50)
        self.thread_spin.setValue(10)
        thread_layout.addWidget(thread_label)
        thread_layout.addWidget(self.thread_spin)
        thread_layout.addStretch()
        settings_layout.addLayout(thread_layout)
        
        # Feedtime
        feedtime_layout = QHBoxLayout()
        feedtime_label = QLabel("Feedtime (ms):")
        feedtime_label.setMinimumWidth(100)
        self.feedtime_spin = QSpinBox()
        self.feedtime_spin.setMinimum(0)
        self.feedtime_spin.setMaximum(5000)
        self.feedtime_spin.setValue(450)
        feedtime_layout.addWidget(feedtime_label)
        feedtime_layout.addWidget(self.feedtime_spin)
        feedtime_layout.addStretch()
        settings_layout.addLayout(feedtime_layout)
        
        # Otomatik Optimizasyon Butonu
        optimize_layout = QHBoxLayout()
        self.optimize_button = QPushButton("⚡ Otomatik Optimizasyon (Ping Testi)")
        self.optimize_button.setObjectName("optimizeButton")
        self.optimize_button.setMinimumHeight(35)
        self.optimize_button.setToolTip("Bağlantı hızına göre Feed Time ve Thread Aralığını optimize eder")
        self.optimize_button.clicked.connect(self.auto_optimize_settings)
        optimize_layout.addWidget(self.optimize_button)
        settings_layout.addLayout(optimize_layout)
        
        settings_group.setLayout(settings_layout)
        main_layout.addWidget(settings_group)
        
        # Gelişmiş Ayarlar Butonu
        advanced_button_layout = QHBoxLayout()
        self.advanced_button = QPushButton("🔧 Gelişmiş Ayarlar...")
        self.advanced_button.setObjectName("advancedButton")
        self.advanced_button.setMinimumHeight(40)
        self.advanced_button.clicked.connect(self.open_advanced_settings)
        advanced_button_layout.addWidget(self.advanced_button)
        main_layout.addLayout(advanced_button_layout)
        
        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        main_layout.addWidget(self.progress_bar)
        
        # Log Alanı
        log_group = QGroupBox("📋 İşlem Günlüğü")
        log_group.setObjectName("groupBox")
        log_layout = QVBoxLayout()
        
        # Log dosya yolu bilgisi
        log_file_info = QLabel(f"📁 Loglar kaydediliyor: {os.path.basename(self.log_file_path)}")
        log_file_info.setStyleSheet("""
            QLabel {
                color: #00d2ff;
                font-size: 10px;
                padding: 2px;
                background: transparent;
            }
        """)
        log_file_info.setToolTip(self.log_file_path)
        log_layout.addWidget(log_file_info)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMinimumHeight(250)
        log_layout.addWidget(self.log_text)
        
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)
        
        # Kontrol Butonları
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("🚀 Başlat")
        self.start_button.setObjectName("startButton")
        self.start_button.setMinimumHeight(45)
        self.start_button.clicked.connect(self.start_process)
        
        self.stop_button = QPushButton("⛔ Durdur")
        self.stop_button.setObjectName("stopButton")
        self.stop_button.setMinimumHeight(45)
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_process)
        
        self.test_button = QPushButton("🧪 Test Et")
        self.test_button.setObjectName("testButton")
        self.test_button.setMinimumHeight(45)
        self.test_button.clicked.connect(self.test_process)
        
        self.clear_button = QPushButton("🗑️ Temizle")
        self.clear_button.setObjectName("clearButton")
        self.clear_button.setMinimumHeight(45)
        self.clear_button.clicked.connect(self.clear_log)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.test_button)
        button_layout.addWidget(self.clear_button)
        
        main_layout.addLayout(button_layout)
        
        # Footer - Telif Hakkı Bilgisi
        footer_frame = QFrame()
        footer_frame.setFrameShape(QFrame.NoFrame)
        footer_frame.setStyleSheet("""
            QFrame {
                background: transparent;
                border: none;
                padding: 0px;
                margin-top: 0px;
            }
        """)
        footer_layout = QHBoxLayout(footer_frame)
        footer_layout.setContentsMargins(5, 0, 5, 0)
        
        # Logo/Icon
        footer_icon = QLabel("🔐")
        footer_icon.setStyleSheet("font-size: 16px; background: transparent; border: none;")
        footer_layout.addWidget(footer_icon)
        
        # Tek satırda copyright metni
        copyright_label = QLabel(
            '© 2026 <a href="https://forum.miuiturkiye.net/uyeler/serdaronline.99036/" '
            'style="color: #00d2ff; text-decoration: none;">SerdarOnline</a> | '
            '<a href="https://forum.miuiturkiye.net/" '
            'style="color: #3a7bd5; text-decoration: none;">MiuiTürkiye</a>'
        )
        copyright_label.setOpenExternalLinks(True)
        copyright_label.setStyleSheet("""
            QLabel {
                color: #b0b3c1;
                font-size: 11px;
                background: transparent;
                border: none;
            }
        """)
        footer_layout.addWidget(copyright_label)
        
        footer_layout.addStretch()
        
        # Versiyon
        version_label = QLabel("v1.0.0")
        version_label.setStyleSheet("""
            QLabel {
                color: #3a7bd5;
                font-size: 10px;
                font-weight: bold;
                background: transparent;
                border: none;
            }
        """)
        footer_layout.addWidget(version_label)
        
        main_layout.addWidget(footer_frame)
        
        # Durum Çubuğu
        self.statusBar().showMessage("Hazır - By SerdarOnline")
        
        # System Tray Icon
        self.setup_tray_icon()
        
        # Başlangıç log mesajları
        self.add_log("🚀 Program başlatıldı - HyperOS Bootloader Unlocker v1.0.0", "success")
        self.add_log(f"📁 Log dosyası: {self.log_file_path}", "info")
        self.add_log("ℹ️ Tüm işlem günlükleri otomatik olarak kaydediliyor", "info")
        
    def setup_tray_icon(self):
        """System tray icon'u kur"""
        # İkon yolu
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "xiaomi.ico")
        
        # Tray icon oluştur
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(icon_path))
        self.tray_icon.setToolTip("HyperOS Bootloader Unlocker")
        
        # Tray menü oluştur
        tray_menu = QMenu()
        
        # Göster/Gizle
        show_action = QAction("Göster", self)
        show_action.triggered.connect(self.show_window)
        tray_menu.addAction(show_action)
        
        hide_action = QAction("Gizle", self)
        hide_action.triggered.connect(self.hide)
        tray_menu.addAction(hide_action)
        
        tray_menu.addSeparator()
        
        # Çıkış
        quit_action = QAction("Çıkış", self)
        quit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        
        # Çift tıklama ile göster
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        
        # Tray icon'u göster
        self.tray_icon.show()
        
    def on_tray_icon_activated(self, reason):
        """Tray icon tıklandığında"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_window()
    
    def show_window(self):
        """Pencereyi göster"""
        self.show()
        self.activateWindow()
        self.raise_()
    
    def quit_application(self):
        """Uygulamayı tamamen kapat"""
        # Log dosyasına kapanış bilgisi yaz
        try:
            with open(self.log_file_path, 'a', encoding='utf-8') as f:
                f.write("\n" + "="*60 + "\n")
                f.write(f"Program Kapandı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*60 + "\n")
        except:
            pass
        
        self.tray_icon.hide()
        QApplication.quit()
    
    def closeEvent(self, event):
        """Pencere kapatıldığında tray'e gönder"""
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "HyperOS Unlocker",
            "Program arka planda çalışmaya devam ediyor. Görevi açmak için simgeye çift tıklayın.",
            QSystemTrayIcon.Information,
            2000
        )
        
    def get_stylesheet(self):
        """Premium Modern Tema - Dark Accent"""
        return """
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #1a1c2e, stop:1 #2d3250);
            }
            
            QLabel#title {
                font-size: 32px;
                font-weight: bold;
                padding: 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #3a7bd5, stop:1 #00d2ff);
                border-radius: 12px;
                color: white;
                text-transform: uppercase;
                letter-spacing: 2px;
            }
            
            QGroupBox {
                font-size: 15px;
                font-weight: bold;
                border: 2px solid #3d4463;
                border-radius: 12px;
                margin-top: 12px;
                padding-top: 15px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #252842, stop:1 #1e1f35);
            }
            
            QGroupBox::title {
                color: #00d2ff;
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 8px;
                font-weight: 600;
            }
            
            QLineEdit, QSpinBox {
                padding: 10px 15px;
                border: 2px solid #3d4463;
                border-radius: 8px;
                background-color: #1e1f35;
                color: #e8e8e8;
                font-size: 13px;
                selection-background-color: #3a7bd5;
            }
            
            QSpinBox::up-button, QSpinBox::down-button {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #3d4463, stop:1 #2d3250);
                border: none;
                border-radius: 4px;
                width: 20px;
                margin: 3px;
            }
            
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #4d5473, stop:1 #3d4260);
            }
            
            QSpinBox::up-button:pressed, QSpinBox::down-button:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #2d3443, stop:1 #1d2240);
            }
            
            QSpinBox::up-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-bottom: 5px solid #00d2ff;
                width: 0;
                height: 0;
            }
            
            QSpinBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 5px solid #00d2ff;
                width: 0;
                height: 0;
            }
            
            QLineEdit:focus, QSpinBox:focus {
                border: 2px solid #00d2ff;
                background-color: #252842;
            }
            
            QLabel {
                color: #b8b8d1;
                font-size: 13px;
                font-weight: 500;
            }
            
            QPushButton {
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                color: white;
            }
            
            QPushButton#startButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #0ba360, stop:1 #3cba92);
            }
            
            QPushButton#startButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #0d9454, stop:1 #36a884);
            }
            
            QPushButton#startButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #087543, stop:1 #2a8665);
            }
            
            QPushButton#startButton:disabled {
                background-color: #4a4c5e;
                color: #7a7a8a;
            }
            
            QPushButton#stopButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #eb3349, stop:1 #f45c43);
            }
            
            QPushButton#stopButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #d42d3f, stop:1 #db4a39);
            }
            
            QPushButton#stopButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #bd1f2f, stop:1 #c23b2d);
            }
            
            QPushButton#stopButton:disabled {
                background-color: #4a4c5e;
                color: #7a7a8a;
            }
            
            QPushButton#clearButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #667eea, stop:1 #764ba2);
            }
            
            QPushButton#clearButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #5568d3, stop:1 #643d8a);
            }
            
            QPushButton#clearButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #4552bb, stop:1 #522f72);
            }
            
            QPushButton#autoTokenButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #fa709a, stop:1 #fee140);
            }
            
            QPushButton#autoTokenButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #e8608a, stop:1 #eed530);
            }
            
            QPushButton#autoTokenButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #d6507a, stop:1 #dcc920);
            }
            
            QPushButton#advancedButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #667eea, stop:1 #764ba2);
                color: white;
                font-weight: bold;
            }
            
            QPushButton#advancedButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #556eda, stop:1 #663b92);
            }
            
            QPushButton#advancedButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #445eca, stop:1 #562b82);
            }
            
            QPushButton#optimizeButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #f093fb, stop:1 #f5576c);
                color: white;
                font-weight: bold;
            }
            
            QPushButton#optimizeButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #e083eb, stop:1 #e5475c);
            }
            
            QPushButton#optimizeButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #d073db, stop:1 #d5374c);
            }
            
            QPushButton#testButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #ff9a56, stop:1 #ffce54);
                color: #1a1c2e;
            }
            
            QPushButton#testButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #e88a46, stop:1 #e8be44);
            }
            
            QPushButton#testButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #d07a36, stop:1 #d0ae34);
            }
            
            QTextEdit {
                border: 2px solid #3d4463;
                border-radius: 8px;
                background-color: #0d0e1a;
                color: #e8e8e8;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
                padding: 10px;
                selection-background-color: #3a7bd5;
            }
            
            /* Scrollbar Stilleri */
            QScrollBar:vertical {
                background: #1e1f35;
                width: 12px;
                border-radius: 6px;
                margin: 0px;
            }
            
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #3a7bd5, stop:1 #00d2ff);
                border-radius: 6px;
                min-height: 30px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #4a8be5, stop:1 #10e2ff);
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            
            QScrollBar:horizontal {
                background: #1e1f35;
                height: 12px;
                border-radius: 6px;
                margin: 0px;
            }
            
            QScrollBar::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #3a7bd5, stop:1 #00d2ff);
                border-radius: 6px;
                min-width: 30px;
            }
            
            QScrollBar::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #4a8be5, stop:1 #10e2ff);
            }
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
            
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
            
            QProgressBar {
                border: 2px solid #3d4463;
                border-radius: 8px;
                text-align: center;
                background-color: #1e1f35;
                height: 32px;
                font-weight: bold;
                font-size: 13px;
                color: #e8e8e8;
            }
            
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #3a7bd5, stop:1 #00d2ff);
                border-radius: 6px;
                margin: 2px;
            }
            
            QStatusBar {
                background-color: #1e1f35;
                color: #b8b8d1;
                border-top: 2px solid #3d4463;
                font-size: 12px;
            }
            
            /* QMessageBox için stil */
            QMessageBox {
                background-color: #252842;
            }
            
            QMessageBox QLabel {
                color: #e8e8e8;
                font-size: 13px;
            }
            
            QMessageBox QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #3a7bd5, stop:1 #00d2ff);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-size: 13px;
                font-weight: bold;
                min-width: 80px;
            }
            
            QMessageBox QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #2a6bc5, stop:1 #00c2ef);
            }
            
            QMessageBox QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #1a5bb5, stop:1 #00b2df);
            }
        """
    
    def open_advanced_settings(self):
        """Gelişmiş ayarlar popup'ını aç"""
        dialog = AdvancedSettingsDialog(self, self.advanced_settings)
        if dialog.exec_() == QDialog.Accepted:
            # Ayarları güncelle
            self.advanced_settings = dialog.get_settings()
            self.add_log("✅ Gelişmiş ayarlar güncellendi", "success")
    
    def auto_optimize_settings(self):
        """Bağlantı hızına göre otomatik optimizasyon"""
        self.optimize_button.setEnabled(False)
        self.optimize_button.setText("⏳ Test ediliyor...")
        self.add_log("📡 Bağlantı hızı ölçülüyor...", "info")
        
        QApplication.processEvents()  # UI güncellenmesini sağla
        
        try:
            import urllib3
            http = urllib3.PoolManager(timeout=urllib3.Timeout(connect=3.0, read=3.0))
            
            # Singapur endpoint'e ping at
            endpoints = [
                "https://sgp-api.buy.mi.com"
            ]
            
            ping_times = []
            for endpoint in endpoints:
                try:
                    start = time.time()
                    http.request('HEAD', endpoint, timeout=3.0)
                    ping_ms = (time.time() - start) * 1000
                    ping_times.append(ping_ms)
                    self.add_log(f"📍 {endpoint.split('/')[2]}: {ping_ms:.0f}ms", "info")
                except:
                    pass
            
            if not ping_times:
                self.add_log("❌ Ping testi başarısız, varsayılan değerler kullanılıyor", "error")
                return
            
            avg_ping = sum(ping_times) / len(ping_times)
            self.add_log(f"📊 Ortalama Ping: {avg_ping:.0f}ms", "info")
            
            # Ping'e göre optimal değerleri hesapla
            if avg_ping < 50:
                # Çok hızlı bağlantı
                optimal_feedtime = 300
                optimal_stagger = 3
                connection_type = "🚀 Mükemmel"
            elif avg_ping < 100:
                # İyi bağlantı
                optimal_feedtime = 400
                optimal_stagger = 5
                connection_type = "✅ Çok İyi"
            elif avg_ping < 150:
                # Orta bağlantı
                optimal_feedtime = 500
                optimal_stagger = 7
                connection_type = "🟡 İyi"
            elif avg_ping < 250:
                # Yavaş bağlantı
                optimal_feedtime = 600
                optimal_stagger = 10
                connection_type = "🟠 Orta"
            else:
                # Çok yavaş bağlantı
                optimal_feedtime = 750
                optimal_stagger = 15
                connection_type = "🔴 Yavaş"
            
            # Değerleri güncelle
            self.feedtime_spin.setValue(optimal_feedtime)
            self.advanced_settings['staggered_delay_ms'] = optimal_stagger
            
            self.add_log(f"✨ Optimizasyon Tamamlandı!", "success")
            self.add_log(f"   Bağlantı: {connection_type} ({avg_ping:.0f}ms)", "success")
            self.add_log(f"   Feed Time: {optimal_feedtime}ms", "success")
            self.add_log(f"   Thread Aralığı: {optimal_stagger}ms", "success")
            
            QMessageBox.information(
                self, 
                "✨ Optimizasyon Tamamlandı",
                f"Bağlantı Kalitesi: {connection_type}\n"
                f"Ortalama Ping: {avg_ping:.0f}ms\n\n"
                f"⚙️ Optimal Ayarlar:\n"
                f"Feed Time: {optimal_feedtime}ms\n"
                f"Thread Aralığı: {optimal_stagger}ms\n\n"
                f"Bu ayarlar otomatik olarak uygulandı."
            )
            
        except Exception as e:
            self.add_log(f"❌ Optimizasyon hatası: {e}", "error")
        
        finally:
            self.optimize_button.setEnabled(True)
            self.optimize_button.setText("⚡ Otomatik Optimizasyon (Ping Testi)")
    
    def add_log(self, message, log_type="info"):
        """Renkli log ekleme ve dosyaya kaydetme"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        full_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        color_map = {
            "info": "#17a2b8",      # cyan
            "success": "#28a745",   # green
            "warning": "#ffc107",   # yellow
            "error": "#dc3545"      # red
        }
        
        # Ekrana renkli göster
        color = color_map.get(log_type, "#f8f9fa")
        html = f'<span style="color: {color};">[{timestamp}] {message}</span>'
        self.log_text.append(html)
        
        # Auto-scroll
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
        # Dosyaya düz metin olarak kaydet
        try:
            with open(self.log_file_path, 'a', encoding='utf-8') as f:
                # HTML etiketlerini temizle
                clean_message = re.sub('<[^<]+?>', '', message)
                f.write(f"[{full_timestamp}] [{log_type.upper()}] {clean_message}\n")
        except Exception as e:
            # Log dosyasına yazma hatası olursa sadece ekrana yazmaya devam et
            pass
        
    def start_process(self):
        """İşlemi başlat"""
        token = self.token_input.text().strip()
        user_id = self.userid_input.text().strip()
        
        if not token or not user_id:
            QMessageBox.warning(self, "Uyarı", "Lütfen Token ve User ID alanlarını doldurun!")
            return
        
        thread_count = self.thread_spin.value()
        feedtime_ms = self.feedtime_spin.value()
        
        # Gelişmiş ayarları kullan (popup'tan kaydedilmiş)
        advanced_settings = self.advanced_settings
        
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.test_button.setEnabled(False)
        self.statusBar().showMessage("İşlem başlatıldı...")
        
        self.add_log("İşlem başlatılıyor...", "info")
        
        # Worker thread oluştur
        self.worker = WorkerThread(token, user_id, thread_count, feedtime_ms, test_mode=False, advanced_settings=advanced_settings)
        self.worker.log_signal.connect(self.add_log)
        self.worker.progress_signal.connect(self.progress_bar.setValue)
        self.worker.finished_signal.connect(self.on_process_finished)
        self.worker.start()
        
    def stop_process(self):
        """İşlemi durdur"""
        if self.worker and self.worker.isRunning():
            self.add_log("İşlem durduruluyor...", "warning")
            self.worker.stop()
            self.worker.wait()
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.test_button.setEnabled(True)
            self.statusBar().showMessage("İşlem durduruldu")
    
    def test_process(self):
        """Test modu - Zaman beklemeden direkt istek gönder"""
        token = self.token_input.text().strip()
        user_id = self.userid_input.text().strip()
        
        if not token or not user_id:
            QMessageBox.warning(self, "Uyarı", "Lütfen Token ve User ID alanlarını doldurun!")
            return
        
        thread_count = self.thread_spin.value()
        feedtime_ms = self.feedtime_spin.value()
        
        # Gelişmiş ayarları kullan (popup'tan kaydedilmiş)
        advanced_settings = self.advanced_settings
        
        self.start_button.setEnabled(False)
        self.test_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.statusBar().showMessage("Test işlemi başlatıldı...")
        
        self.add_log("🧪 TEST MODU - Zaman beklemeden direkt istek gönderiliyor...", "warning")
        
        # Worker thread oluştur (test mode)
        self.worker = WorkerThread(token, user_id, thread_count, feedtime_ms, test_mode=True, advanced_settings=advanced_settings)
        self.worker.log_signal.connect(self.add_log)
        self.worker.progress_signal.connect(self.progress_bar.setValue)
        self.worker.finished_signal.connect(self.on_process_finished)
        self.worker.start()
            
    def on_process_finished(self, success, message):
        """İşlem tamamlandığında"""
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.test_button.setEnabled(True)
        
        if success:
            QMessageBox.information(self, "Başarılı", message)
            self.statusBar().showMessage("İşlem başarıyla tamamlandı!")
        else:
            self.statusBar().showMessage("İşlem tamamlandı")
            
    def clear_log(self):
        """Log'u temizle"""
        self.log_text.clear()
        self.progress_bar.setValue(0)
        # Dosyaya ayırıcı yaz
        try:
            with open(self.log_file_path, 'a', encoding='utf-8') as f:
                f.write("\n" + "-"*60 + "\n")
                f.write("LOG TEMİZLENDİ - Yeni Oturum Başladı\n")
                f.write("-"*60 + "\n\n")
        except:
            pass
        self.add_log("Log ekranı temizlendi", "info")
    
    def fetch_token_automatically(self):
        """Selenium ile otomatik token çekme"""
        self.auto_token_button.setEnabled(False)
        self.add_log("🔍 Otomatik token alma işlemi başlatılıyor...", "info")
        
        # Token fetcher thread oluştur
        self.token_fetcher = TokenFetcherThread()
        self.token_fetcher.log_signal.connect(self.add_log)
        self.token_fetcher.success_signal.connect(self.on_token_fetched)
        self.token_fetcher.error_signal.connect(self.on_token_fetch_error)
        self.token_fetcher.finished.connect(lambda: self.auto_token_button.setEnabled(True))
        self.token_fetcher.start()
    
    def on_token_fetched(self, token, user_id):
        """Token başarıyla alındığında"""
        self.token_input.setText(token)
        self.userid_input.setText(user_id)
        self.add_log("✅ Token ve User ID otomatik olarak alındı!", "success")
        QMessageBox.information(self, "Başarılı", "Token ve User ID başarıyla alındı!")
    
    def on_token_fetch_error(self, error_msg):
        """Token alma hatası"""
        QMessageBox.warning(self, "Hata", error_msg)


def main():
    # 🔒 Lisans Doğrulama - By SerdarOnline
    _check_author_integrity()
    
    # Qt plugin path'i ayarla (venv için gerekli)
    if getattr(sys, 'frozen', False):
        # PyInstaller ile paketlenmişse
        qt_plugin_path = os.path.join(sys._MEIPASS, 'PyQt5', 'Qt5', 'plugins')
        os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qt_plugin_path
    else:
        # Geliştirme ortamında - birden fazla path'i dene
        python_dir = os.path.dirname(sys.executable)
        possible_paths = [
            os.path.join(python_dir, 'Lib', 'site-packages', 'PyQt5', 'Qt5', 'plugins'),
            os.path.join(os.path.dirname(__file__), '.venv', 'Lib', 'site-packages', 'PyQt5', 'Qt5', 'plugins'),
        ]
        
        # site-packages locations
        try:
            import site
            for sp in site.getsitepackages():
                possible_paths.append(os.path.join(sp, 'PyQt5', 'Qt5', 'plugins'))
        except:
            pass
        
        # İlk var olan path'i kullan
        for qt_plugin_path in possible_paths:
            if os.path.exists(qt_plugin_path):
                os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qt_plugin_path
                break
    
    # Windows taskbar için AppUserModelID ayarla
    if sys.platform == 'win32':
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('hyperosunlocker.app.1.0')
    
    # Yüksek DPI desteği - QApplication oluşturulmadan önce ayarlanmalı
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    
    # İkon yolunu ayarla
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "xiaomi.ico")
    app.setWindowIcon(QIcon(icon_path))
    
    # Uygulama font ayarları
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # 🎨 SPLASH SCREEN - MiuiTürkiye Forum
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "forum_logo.png")
    if os.path.exists(logo_path):
        pixmap = QPixmap(logo_path)
        # Logo'yu ölçeklendir (maksimum 400x400)
        if pixmap.width() > 400 or pixmap.height() > 400:
            pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
        
        # Splash screen'e metin ekle
        splash.setStyleSheet("""
            QSplashScreen {
                background-color: #1a1c2e;
                border: 3px solid #3a7bd5;
                border-radius: 15px;
            }
        """)
        
        # Mesajları göster
        splash.show()
        splash.showMessage(
            "\n\n\n\n\n\n\n\n\n\n"
            "HyperOS Bootloader Unlocker\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Yazar: SerdarOnline\n"
            "Forum: MiuiTürkiye\n\n"
            "Yükleniyor...",
            Qt.AlignCenter | Qt.AlignBottom,
            Qt.white
        )
        app.processEvents()
        
        # Splash screen'i 3 saniye göster
        QTimer.singleShot(3000, splash.close)
        
        # Ana pencereyi splash kapandıktan sonra göster
        window = HyperOSUnlockerGUI()
        QTimer.singleShot(3000, window.show)
    else:
        # Logo yoksa direkt aç
        window = HyperOSUnlockerGUI()
        window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

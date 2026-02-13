# 🔓 HyperOS Bootloader Unlocker v1.2.0 (Pro GUI Edition)

<div align="center">

![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)
![License](https://img.shields.io/badge/license-Proprietary-red.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)

**Xiaomi HyperOS cihazlar için milisaniyelik hassasiyete sahip profesyonel bootloader kilit açma aracı**

[MiuiTürkiye Forum](https://forum.miuiturkiye.net/) | [SerdarOnline](https://forum.miuiturkiye.net/uyeler/serdaronline.99036/)

</div>

---

## 🔱 Kaynak ve Teşekkür

Bu proje, **[pwnj/auto-hyperos-unlocker](https://github.com/pwnj/auto-hyperos-unlocker)** projesinden esinlenilerek ve temelleri üzerine inşa edilerek geliştirilmiştir. Orijinal mantık ve API keşifleri için **pwnj**'ye teşekkürlerimi sunarım.

**Forked & Enhanced by SerdarOnline:** Bu sürüm, orijinal scriptin üzerine profesyonel bir **PyQt5 GUI**, **Kalıcı Log Sistemi**, **Otomatik Optimizasyon**, **System Tray Desteği** ve **Otomatik Token Çekici** eklenmiş geliştirilmiş halidir.

**MiuiTürkiye Community Edition** - Türk Xiaomi topluluğu için optimize edilmiş.

---

## ✨ Öne Çıkan Özellikler

### 🖥️ **Modern Arayüz**
* **PyQt5 GUI:** Kullanımı kolay, profesyonel karanlık tema
* **Canlı Log:** Renkli ve detaylı işlem günlüğü
* 📁 **Kalıcı Log Sistemi** - Tüm işlemler EXE'nin yanında `logs/` klasörüne kaydedilir
* **System Tray:** Arka planda çalışma desteği
* **Splash Screen:** MiuiTürkiye forum logosu ile profesyonel açılış

### 🕒 **Milisaniyelik Hassasiyet**
* **NTP Zaman Senkronizasyonu:** Pekin atomik saati ile milisaniyelik tam uyum
* **Feed Time Kontrolü:** İnternet hızınıza göre optimize edilebilir (varsayılan: 450ms)
* **Ping Ölçümü:** Endpoint'lere gerçek zamanlı ping testi

### 🌍 **Global Multi-Region Desteği**
* **Singapur API:** Ana endpoint (doğrulanmış ve çalışıyor) ✅
* **Akıllı Failover:** Bir sunucu hata verirse otomatik yedek sunucuya geçiş
* **Connection Pre-warming:** TCP/SSL bağlantılarını önceden ısıtma

### 🔑 **Otomatik Token Sistemi**
* **Selenium Auto-Login:** Token ve User ID'yi otomatik çeker
* **ChromeDriver Auto-Manager:** webdriver-manager ile otomatik uyumlu sürüm indirme
* **Bot Protection Bypass:** Gelişmiş Chrome seçenekleri ile bot algılama önleme
* **Manuel Giriş:** İsteğe bağlı manuel token girişi
* **Interactive CLI:** CLI versiyonunda interaktif token girişi

### ⚡ **Akıllı Optimizasyon**
* **Otomatik Ping Testi:** Bağlantı kalitesine göre ayar önerisi
* **Gelişmiş Ayarlar:** Failover, timeout, thread aralığı konfigürasyonu
* **Test Modu:** Zaman beklemeden direkt test etme

### 💻 **Dual Mode**
* **GUI Version:** Grafiksel arayüz ile kolay kullanım (önerilen)
* **CLI Version:** Komut satırı için hafif versiyon
* **Her iki versiyon da log kaydı yapıyor**

---

## 📖 İçindekiler

- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım-kılavuzu)
- [Log Sistemi](#-log-sistemi-v120)
- [Gelişmiş Ayarlar](#-gelişmiş-ayarlar)
- [Sorun Giderme](#-sorun-giderme)
- [Değişiklik Günlüğü](#-değişiklik-günlüğü)
- [Lisans](#-lisans)

---

## �️ Kurulum

### 📥 Windows Kullanıcıları (Önerilen)

**EXE ile Kullanım (Kurulum Gerektirmez):**
1. Release sayfasından `HyperOSUnlocker.exe` dosyasını indirin
2. Dosyayı çift tıklayarak çalıştırın
3. Windows Defender uyarısı gelirse: "Daha fazla bilgi" → "Yine de çalıştır"

> 💡 EXE dosyası PyInstaller ile paketlenmiştir. Kaynak kod tamamen açık ve incelenebilir.

### 🐍 Python ile Çalıştırma

1. Python 3.8 veya üzeri bir sürümün yüklü olduğundan emin olun
2. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
3. **GUI** uygulamasını çalıştırın:
   ```bash
   python hyperosunlocker_gui.py
   ```
4. **CLI** versiyonunu çalıştırın:
   ```bash
   python hyperosunlocker.py
   ```

**Gerekli Paketler:**
- `PyQt5==5.15.10` - GUI framework
- `selenium==4.16.0` + `webdriver-manager==4.0.2` - Otomatik token alma ve ChromeDriver yönetimi
- `urllib3==2.1.0`, `ntplib==0.4.0`, `pytz==2024.1` - Network & Time sync

---

## � Kullanım Kılavuzu

### 🖥️ GUI Versiyonu (Önerilen)

#### **Hızlı Başlangıç:**

1. **Token Al:**
   - Uygulamayı açın ve **"🔑 Otomatik Token ve User ID Al"** butonuna tıklayın
   - Açılan Chrome penceresinde **Xiaomi Community** hesabınıza giriş yapın
   - Token ve User ID otomatik alınacak ve kutulara yazılacak

2. **Ayarlar:**
   - **Thread Sayısı:** İnternet hızınıza göre 10-20 arası önerilir
   - **Feed Time (ms):** İnternet pinginize göre 400-500ms arası idealdir
   - **⚡ Otomatik Optimizasyon** butonu ile ping testi yapıp otomatik ayarlayabilirsiniz

3. **Gelişmiş Ayarlar (İsteğe Bağlı):**
   - **"🔧 Gelişmiş Ayarlar..."** butonuyla failover, timeout ayarlarını yapılandırın

4. **Başlat:**
   - Saat **23:59:00** civarında **"🚀 Başlat"** butonuna basın
   - Program otomatik olarak:
     - ⏰ Pekin saati ile senkronize olacak
     - 📡 Ping testi yapacak
     - ⏳ Gece 00:00'a kadar bekleyecek
     - 🚀 Feed Time süresinde önce istekleri gönderecek

5. **İzle:**
   - Log ekranından sunucu yanıtlarını ve milisaniyeleri takip edin
   - 📁 Tüm işlemler otomatik olarak `logs/` klasörüne kaydedilir

#### **Test Modu:**
- **"🧪 Test Et"** butonuyla zaman beklemeden direkt test edebilirsiniz
- Kotanızı kullanmadan sistem kontrolü yapabilirsiniz

---

### 💻 CLI Versiyonu

#### **Yöntem 1: İnteraktif Giriş (Önerilen)**
```bash
python hyperosunlocker.py
```
Program açıldığında menüden **"1"** seçip TOKEN'ı girebilirsiniz.

#### **Yöntem 2: Kod İçinde Ayarlama**
`hyperosunlocker.py` dosyasını açın ve değerleri güncelleyin:
```python
TOKEN = "your_token_here"
USER_ID = "your_user_id_here"
THREAD_COUNT = 10
FEEDTIME_MS = 450
```

Ardından çalıştırın:
```bash
python hyperosunlocker.py
```

---

## 📁 Log Sistemi (v1.2.0)

### Otomatik Log Kaydı

Program çalıştığında **EXE'nin yanında** otomatik olarak `logs/` klasörü oluşturur ve tüm işlemleri kaydeder.

#### GUI Log Formatı:
```
logs/hyperosunlocker_20260210_143055.log
```

#### CLI Log Formatı:
```
logs/hyperosunlocker_cli_20260210_143055.log
```

### Log Dosyası İçeriği

```log
============================================================
HyperOS Bootloader Unlocker - Log Dosyası
Başlangıç: 2026-02-10 14:30:55
Copyright © 2026 SerdarOnline
============================================================

[2026-02-10 14:30:55] [SUCCESS] 🚀 Program başlatıldı - HyperOS Bootloader Unlocker v1.1.0
[2026-02-10 14:30:55] [INFO] 📁 Log dosyası: C:\...\logs\hyperosunlocker_20260210_143055.log
[2026-02-10 14:30:56] [INFO] ⏰ Zaman senkronize ediliyor...
[2026-02-10 14:30:57] [SUCCESS] ✅ Pekin Saati: 22:30:57
[2026-02-10 14:30:58] [INFO] 📡 SGP API Ping: 89ms
[2026-02-10 14:30:59] [INFO] 🎯 Hedef Saat: 00:00:00
[2026-02-10 14:30:59] [INFO] 🚀 Tetiklenme: 23:59:59.550
...
[2026-02-10 23:59:59] [INFO] [Thread-0] Başvuru gönderiliyor...
[2026-02-10 23:59:59] [SUCCESS] ✅ Token bulundu
[2026-02-10 23:59:59] [SUCCESS] 🎉 BAŞARILI! Kilit açma izni alındı!

============================================================
Program Kapandı: 2026-02-10 15:22:10
============================================================
```

### Log Özellikleri

- ✅ **Timestamp:** Her satırda tarih ve saat
- ✅ **Log Level:** INFO, SUCCESS, WARNING, ERROR
- ✅ **Emoji Korunur:** Dosyada da emoji karakterler var
- ✅ **Session Lifecycle:** Başlangıç ve bitiş logları
- ✅ **Clean Text:** HTML/ANSI kodları temizlenmiş
- ✅ **Ctrl+C Safe:** Program kapatılırken bile log kaydedilir
- ✅ **Unique Filenames:** Timestamped - eski loglar silinmez

### Log Kullanımı

**GUI'de Log Dosya Bilgisi:**
- Ana pencerede `📁 Loglar kaydediliyor: hyperosunlocker_YYYYMMDD_HHMMSS.log` yazısı görünür
- Fare ile üzerine gelince tam dosya yolu gösterilir

**Log Temizleme:**
- **"🗑️ Temizle"** butonu sadece ekranı temizler
- Dosyada session separator eklenir:
  ```
  ------------------------------------------------------------
  LOG TEMİZLENDİ - Yeni Oturum Başladı
  ------------------------------------------------------------
  ```

**Log Analizi:**
```bash
# Hata loglarını filtreleme
findstr "ERROR" logs\hyperosunlocker_20260210_143055.log

# Başarılı istekleri görme
findstr "BAŞARILI" logs\hyperosunlocker_20260210_143055.log

# Thread aktivitelerini takip
findstr "Thread" logs\hyperosunlocker_20260210_143055.log
```

---

## 🔧 Gelişmiş Ayarlar

### Ayarlar Paneli

**"🔧 Gelişmiş Ayarlar..."** butonu ile açılan popup'ta:

#### 1. **Failover Denemesi** (1-5)
- Bir sunucu hata verdiğinde kaç farklı bölge denenir
- Varsayılan: **2 deneme**
- Yüksek değerler daha fazla failover sağlar

#### 2. **Thread Aralığı** (0-50ms)
- Her thread arasındaki başlatma gecikmesi
- Varsayılan: **5ms**
- Düşük ping: 3ms | Yüksek ping: 10-15ms

#### 3. **İstek Timeout** (1-10 saniye)
- HTTP istekleri için maksimum bekleme
- Varsayılan: **2 saniye**
- Yavaş bağlantı: 3-5 saniye | Hızlı: 1-2 saniye

#### 4. **DNS Ön Belleğe Alma** (✓/✗)
- Program başlamadan önce DNS çözümlemesi yapar
- Varsayılan: **Aktif**
- İlk isteklerde gecikme önler

#### 5. **Kullanılacak Bölgeler**
- 🇸🇬 **Singapur API** (SADECE BU ÇALIŞIYOR) ✅
- Diğer endpoint'ler şu anda devre dışı

> ⚠️ **Önemli:** Test sonuçlarına göre sadece Singapur API doğrulanmıştır.

---

## 🔄 Değişiklik Günlüğü

### **v1.2.0** - *13 Şubat 2026* ⭐ **GÜNCEL** ( cloude33 Bildiri için teşekkürler )
- 📂 Log klasörü konumu optimize edildi - EXE'nin yanında `logs/` oluşturulur
- 🔧 ChromeDriver yönetimi iyileştirildi - webdriver-manager standart API kullanımı
- 🛠️ EXE ve script modları için akıllı path detection (sys.frozen kontrolü)
- 🚨 ChromeDriver hata raporlama detaylandırıldı (150 karakter mesaj)
- 💡 Gelişmiş hata çözüm önerileri eklenildi
- 🐛 cache_valid_range uyumluluk sorunu düzeltildi
- 📝 README.md ChromeDriver dokümantasyonu güncellendi

### **v1.1.0** - *10 Şubat 2026*
- 📁 Kalıcı log sistemi - Tüm işlemler `logs/` klasörüne kaydedilir
- 📊 Session lifecycle tracking (başlangıç/bitiş/hata logları)
- 🧹 HTML tag cleaning - Log dosyalarında temiz metin
- 💻 CLI versiyonunda da log desteği
- 📝 Dual output (ekran + dosya)
- 🔄 ChromeDriver otomatik güncelleme - Chrome tarayıcı sürümü ile tam uyum
- 🛡️ Bot protection bypass - Gelişmiş Chrome seçenekleri
- 🚨 Akıllı hata mesajları - ChromeDriver sorunları için detaylı çözümler
- 📦 webdriver-manager 4.0.2 güncellemesi

### **v1.0.0** - *9 Şubat 2026*
- 🖥️ PyQt5 GUI ile profesyonel arayüz
- 🔑 Selenium otomatik token alma
- ⚡ Ping bazlı otomatik optimizasyon
- 🔧 Gelişmiş ayarlar paneli
- 🎬 MiuiTürkiye splash screen
- 🔔 System tray desteği
- 💻 CLI dual mode

---

## ⚠️ Feragatname (Disclaimer)

Bu araç tamamen **eğitim amaçlı** ve Xiaomi'nin resmi başvuru sistemini kolaylaştırmak için yapılmıştır. 

**Önemli Notlar:**
- Hesabınızın başvuru kriterlerini karşılaması gerekir (30 günlük hesap, topluluk puanı vb.)
- Aracın kullanımıyla ilgili sorumluluk kullanıcıya aittir
- Herhangi bir cihaz hasarı, veri kaybı veya garanti kaybından geliştirici sorumlu değildir
- Kullanım riski tamamen kullanıcıya aittir

---

## 🎯 Başarı Sonrası

### Bootloader Kilidi Açma

1. **Mi Unlock Tool İndirin:**
   - [Resmi İndirme Linki](https://en.miui.com/unlock/download_en.html)
   - Windows PC gerekir

2. **Cihazınızı Bağlayın:**
   - USB Debugging açık olmalı
   - Mi Unlock Tool'u çalıştırın
   - Hesabınızla giriş yapın

3. **Kilidi Açın:**
   - "Unlock" butonuna tıklayın
   - Bekleme süresi varsa bekleyin (genelde 168 saat)
   - İzin aldıysanız direkt açılır

4. **Custom ROM Yükleyin:**
   - TWRP Recovery kurun
   - İstediğiniz custom ROM'u flash edin

---

## ❓ Sorun Giderme

### Yaygın Sorunlar ve Çözümleri:

**🔴 "TOKEN ayarlanmamış" Hatası**
- CLI versiyonunda interaktif menüden TOKEN girin veya kod içinde ayarlayın

**🔴 "NTP Hatası" - Zaman Senkronizasyonu**
- İnternet bağlantınızı kontrol edin
- Firewall'un NTP portunu (123/UDP) engellemediğinden emin olun

**🔴 "Kota Dolmuş (Quota Reached)"**
- Günlük kota limitine ulaşmışsınız
- Bu program tam da bu sorunu çözmek için tasarlandı - timing çok önemli!

**🔴 Yüksek Ping (>200ms)**
- Feed Time değerini artırın: 600-750ms
- Thread Aralığını 10-15ms yapın
- VPN kullanıyorsanız kapatın

**🔴 Windows Defender Uyarısı**
- "Daha fazla bilgi" → "Yine de çalıştır"
- Kod açık kaynak - incelenebilir

**🔴 Log Dosyası Oluşturulmuyor**
- Program klasöründe yazma izni kontrolü
- Admin olarak çalıştırmayı deneyin

**🔴 "ChromeDriver only supports Chrome version X" Hatası**
- webdriver-manager otomatik olarak uyumlu sürümü indirir
- Eğer hata devam ederse:
  1. Chrome tarayıcınızı güncelleyin: `chrome://settings/help`
  2. ChromeDriver cache'ini manuel temizleyin:
     ```powershell
     Remove-Item -Recurse -Force "$env:USERPROFILE\.wdm\drivers\chromedriver"
     ```
  3. Programı tekrar çalıştırın

**🔴 "Session Not Created" - Tarayıcı Başlatılamıyor**
- webdriver-manager otomatik ChromeDriver yönetimi etkin
- Windows Defender/Antivirus'ün Chrome'u engellemediğinden emin olun
- Chrome tarayıcınızı güncelleyin: `chrome://settings/help`

**🔴 Selenium "No module named 'email'" Hatası**
- Python paketleri eksik, yeniden yükleyin:
  ```bash
  pip install --upgrade -r requirements.txt
  ```

> 💬 **Daha fazla yardım için:** [MiuiTürkiye Forum](https://forum.miuiturkiye.net/) üzerinden SerdarOnline'a mesaj gönderebilirsiniz.

---

## 📄 Lisans

**Copyright © 2026 SerdarOnline. Tüm hakları saklıdır.**

Bu yazılım SerdarOnline tarafından geliştirilmiştir. Telif hakkı koruması altındadır.

**Kullanım Koşulları:**
- ✅ Kişisel kullanım için ücretsiz
- ✅ Kaynak kod incelenebilir
- ❌ Ticari kullanım yasaktır
- ❌ Kod değiştirme ve dağıtma yasaktır
- ❌ Yazar bilgisi silinmesi yasaktır

---

## 🤝 Katkıda Bulunma

Hataları bildirmek veya yeni özellikler eklemek için:
- 🐛 **Bug Raporu:** GitHub Issues
- 💬 **Öneriler:** [MiuiTürkiye Forum](https://forum.miuiturkiye.net/)
- 💻 **Pull Request:** Katkılarınızı bekliyoruz

**Main Repository:** [pwnj/auto-hyperos-unlocker](https://github.com/pwnj/auto-hyperos-unlocker)

---

## 👨‍💻 Geliştirici

**SerdarOnline**  
MiuiTürkiye Forum Üyesi

- 🌐 **Forum:** [MiuiTürkiye](https://forum.miuiturkiye.net/)
- 👤 **Profil:** [SerdarOnline](https://forum.miuiturkiye.net/uyeler/serdaronline.99036/)
- 💬 **Destek:** Forum üzerinden özel mesaj

---

## 🙏 Teşekkürler

- **[pwnj](https://github.com/pwnj)** - Orijinal proje ve API keşifleri için
- **MiuiTürkiye Topluluğu** - Test ve geri bildirimler için
- **Forum Üyeleri** - Destek ve öneriler için
- **Xiaomi Kullanıcıları** - Bootloader özgürlüğü için mücadele edenler

---

<div align="center">

**🔓 HyperOS özgürlüğünün tadını çıkarın!**

*Made with ❤️ by SerdarOnline for MiuiTürkiye Community*

**v1.2.0 - Enhanced & Optimized!** 🚀✨

---

[![MiuiTürkiye](https://img.shields.io/badge/MiuiTürkiye-Forum-FF6600?style=for-the-badge&logo=xiaomi)](https://forum.miuiturkiye.net/)
[![SerdarOnline](https://img.shields.io/badge/Developer-SerdarOnline-blue?style=for-the-badge)](https://forum.miuiturkiye.net/uyeler/serdaronline.99036/)
[![Original](https://img.shields.io/badge/Forked_from-pwnj-green?style=for-the-badge&logo=github)](https://github.com/pwnj/auto-hyperos-unlocker)

</div>

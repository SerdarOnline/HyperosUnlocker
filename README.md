# 🔓 HyperOS Bootloader Unlocker v1.1.0 (Pro GUI Edition)

<div align="center">

![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)
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
* 📁 **Kalıcı Log Sistemi (v1.1.0 YENİ!)** - Tüm işlemler `logs/` klasörüne kaydedilir
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
* **Manuel Giriş:** İsteğe bağlı manuel token girişi
* **Interactive CLI:** CLI versiyonunda interaktif token girişi

### ⚡ **Akıllı Optimizasyon**
* **Otomatik Ping Testi:** Bağlantı kalitesine göre ayar önerisi
* **Gelişmiş Ayarlar:** Failover, timeout, thread aralığı konfigürasyonu
* **Test Modu:** Zaman beklemeden direkt test etme

### 💻 **Dual Mode**
* **GUI Version:** Grafiksel arayüz ile kolay kullanım (önerilen)
* **CLI Version:** Komut satırı için hafif versiyon
* **Her iki versiyon da log kaydı yapıyor** (v1.1.0)

---

## 📖 İçindekiler

- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım-kılavuzu)
- [Log Sistemi (YENİ)](#-log-sistemi-v110)
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
- `PyQt5` - GUI framework
- `selenium` + `webdriver-manager` - Otomatik token alma
- `urllib3`, `ntplib`, `pytz` - Network & Time sync

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

## 📁 Log Sistemi (v1.1.0) ⭐ YENİ

### Otomatik Log Kaydı

Program çalıştığında **otomatik olarak** `logs/` klasörü oluşturur ve tüm işlemleri kaydeder.

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

### 🔴 **"TOKEN ayarlanmamış" Hatası**
**Çözüm:** CLI versiyonunda interaktif menüden TOKEN girin veya kod içinde ayarlayın.

### 🔴 **"NTP Hatası" - Zaman Senkronizasyonu Başarısız**
**Çözüm:**
- İnternet bağlantınızı kontrol edin
- Firewall/Antivirus'ün NTP portunu (123/UDP) engellemediğinden emin olun
- Farklı NTP sunucusu deneyin: `pool.ntp.org` yerine `time.google.com`

### 🔴 **"Kota Dolmuş (Quota Reached)"**
**Çözüm:**
- Günlük kota limitine ulaşmışsınız
- Ertesi gün tekrar deneyin
- Bu program tam da bu kota sınırını atlamak için yapıldı - timing önemli

### 🔴 **Yüksek Ping (>200ms)**
**Çözüm:**
- Feed Time değerini artırın: 600-750ms
- Gelişmiş ayarlardan Thread Aralığını 10-15ms yapın
- İnternet hızınızı kontrol edin
- VPN kullanıyorsanız kapatın

### 🔴 **Windows Defender SmartScreen Uyarısı**
**Çözüm:**
- "Daha fazla bilgi" linkine tıklayın
- "Yine de çalıştır" butonuna basın
- Kod açık kaynak - inceleyebilirsiniz

### 🔴 **Antivirüs Yanlış Pozitif**
**Çözüm:**
- PyInstaller ile paketlenmiş tüm EXE'ler bazı antivirüsler tarafından şüpheli görülebilir
- Kaynak koddan kendiniz derleyebilirsiniz: `python build_exe.py`
- VirusTotal'de tarayabilirsiniz

### 🔴 **Log Dosyası Oluşturulmuyor**
**Çözüm:**
- Program klasöründe yazma izni olduğundan emin olun
- Admin olarak çalıştırmayı deneyin
- `logs/` klasörünü manuel oluşturun

### 🔴 **Token Otomatik Alınmıyor**
**Çözüm:**
- Chrome ve ChromeDriver güncel olmalı
- Xiaomi Community sitesinde düzgün giriş yapın
- Manuel cookie yöntemini kullanın (F12 → Cookies)

---

## 🔄 Değişiklik Günlüğü

### **v1.1.0** - *10 Şubat 2026* ⭐ **YENİ SÜRÜM**

#### 🆕 Yeni Özellikler
- 📁 **Kalıcı Log Sistemi** - Tüm işlemler `logs/` klasörüne kaydedilir
- 📊 **Session Lifecycle Tracking** - Program başlangıç/bitiş/hata logları
- 🧹 **HTML Tag Cleaning** - Log dosyalarında temiz metin formatı
- 💡 **GUI Log Info Label** - Log dosya adı ve yolu bilgisi gösterimi
- 💻 **CLI Log Support** - CLI versiyonunda da log kaydı (`hyperosunlocker_cli_*.log`)
- 📝 **Dual Output System** - Hem ekranda renkli, hem dosyada düz metin

#### 🔧 İyileştirmeler
- Timestamped log dosyaları - her oturum unique isimle
- Ctrl+C ile kapatmada bile log kaydedilir
- Session separator ile oturumlar ayırt edilir
- Program sonunda otomatik footer yazılır
- Log dosyalarında emoji karakterler korunur

---

### **v1.0.0** - *9 Şubat 2026*

#### 🎉 İlk Stabil Sürüm
- 🖥️ PyQt5 tabanlı modern GUI
- 🔑 Selenium ile otomatik token alma
- ⚡ Ping bazlı otomatik optimizasyon
- 🔧 Gelişmiş ayarlar paneli
- 📋 Renkli canlı log sistemi
- 🎬 MiuiTürkiye forum splash screen
- 🔔 System tray (bildirim alanı) desteği
- 💻 CLI versiyon ile dual mode
- 🌍 Singapur API endpoint desteği
- 🔒 Lisans koruma sistemi
- 🛡️ Kod bütünlük doğrulaması

---

## 📊 Sistem Gereksinimleri

### Minimum
- **OS:** Windows 10 (64-bit)
- **RAM:** 512 MB
- **Disk:** 100 MB boş alan
- **İnternet:** Aktif bağlantı

### Önerilen
- **OS:** Windows 11 (64-bit)
- **RAM:** 1 GB
- **İnternet:** 10+ Mbps hız, <100ms ping
- **Python:** 3.8+ (kaynak kod için)

---

## 🔒 Güvenlik

- ✅ **Açık Kaynak** - Tüm kod GitHub'da incelenebilir
- 🔐 **Telif Hakkı Korumalı** - Lisans doğrulama sistemi
- 🛡️ **Kod Bütünlüğü** - MD5 hash ve Base64 imza kontrolü
- 🔍 **Şeffaflık** - Hiçbir veri toplanmaz veya gönderilmez
- 🚫 **Malware-Free** - VirusTotal temiz dosya

---

## 📄 Lisans

**Copyright © 2026 SerdarOnline. Tüm hakları saklıdır.**

### Kullanım Koşulları:

#### ✅ İzin Verilen:
- Kişisel kullanım için ücretsiz
- Kaynak kod incelenebilir
- Eğitim amaçlı kullanım
- MiuiTürkiye topluluğu içinde paylaşım

#### ❌ Yasak:
- Ticari kullanım
- Kod değiştirme ve yeniden dağıtma
- Yazar bilgisini silme/değiştirme
- Kopyalama ve farklı lisans ile yayınlama
- Lisans koruma sistemini kaldırma

### Sorumluluk Reddi:
Bu yazılım eğitim amaçlıdır. Herhangi bir cihaz hasarından, veri kaybından veya garanti kaybından geliştirici sorumlu değildir. Kullanım riski tamamen kullanıcıya aittir.

---

## 👨‍💻 Geliştirici

**SerdarOnline**  
MiuiTürkiye Forum Üyesi

- 🌐 **Forum:** [MiuiTürkiye](https://forum.miuiturkiye.net/)
- 👤 **Profil:** [SerdarOnline](https://forum.miuiturkiye.net/uyeler/serdaronline.99036/)
- 💬 **Destek:** Forum üzerinden özel mesaj

---

## 💬 Destek ve İletişim

### Soru ve Sorun Bildirimi
- 🌐 **Forum:** [MiuiTürkiye](https://forum.miuiturkiye.net/) üzerinden mesaj gönderin
- 💬 **Özel Mesaj:** SerdarOnline'a forum PM
- 🐛 **Bug Raporu:** GitHub Issues sayfası
- 📝 **Log Paylaşımı:** Sorun bildirirken log dosyasını ekleyin

### Topluluk
- MiuiTürkiye forumunda tartışma konusu
- Telegram grubu (yakında)
- Discord sunucusu (planlanan)

---

## 🙏 Teşekkürler

- **MiuiTürkiye Topluluğu** - Test, geri bildirim ve destek için
- **Forum Üyeleri** - Önerileri ve bug raporları için
- **Beta Testerlar** - Erken versiyonları test ettiği için
- **Xiaomi Kullanıcıları** - Bootloader özgürlüğü için mücadele eden herkes

---

## 🌟 Yıldız Verin!

Bu projeyi beğendiyseniz GitHub'da ⭐ vermeyi unutmayın!

---

<div align="center">

**🔓 HyperOS özgürlüğünün tadını çıkarın!**

*Made with ❤️ by SerdarOnline for MiuiTürkiye Community*

**v1.1.0 - Şimdi daha güçlü log sistemiyle!** 📁✨

---

[![MiuiTürkiye](https://img.shields.io/badge/MiuiTürkiye-Forum-FF6600?style=for-the-badge&logo=xiaomi)](https://forum.miuiturkiye.net/)
[![SerdarOnline](https://img.shields.io/badge/Developer-SerdarOnline-blue?style=for-the-badge)](https://forum.miuiturkiye.net/uyeler/serdaronline.99036/)

</div>

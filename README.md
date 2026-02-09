# 🚀 HyperOS Bootloader Unlocker (Pro GUI Edition)

Bu proje, HyperOS Bootloader kilidi açma başvurularındaki "Quota Reached" (Kota Doldu) engelini aşmak için geliştirilmiş, milisaniyelik hassasiyete sahip bir otomasyon aracıdır.

---

### 🔱 Kaynak ve Teşekkür
Bu proje, **[pwnj/auto-hyperos-unlocker](https://github.com/pwnj/auto-hyperos-unlocker)** projesinden esinlenilerek ve temelleri üzerine inşa edilerek geliştirilmiştir. Orijinal mantık ve API keşifleri için **pwnj**'ye teşekkürlerimi sunarım. 

**Forked & Enhanced:** Bu sürüm, orijinal scriptin üzerine profesyonel bir **PyQt5 GUI**, **Çoklu Bölge (Multi-Region) Desteği**, **TCP Pre-warming (Isıtma)** ve **Otomatik Token Çekici** eklenmiş halidir.

---

## ✨ Öne Çıkan Özellikler

* 🖥️ **Modern GUI:** Kullanımı kolay PyQt5 tabanlı grafik arayüzü.
* 🕒 **NTP Zaman Senkronizasyonu:** Pekin atomik saati ile milisaniyelik tam uyum.
* 🌍 **Global Multi-Region:** Tek noktadan değil; Singapur, Rusya, Avrupa ve Hindistan sunucularından aynı anda başvuru.
* 🔥 **Bağlantı Isıtma (Pre-warming):** Saat 19:00 olmadan önce TCP/SSL tünellerini hazır tutarak gecikmeyi (latency) minimize eder.
* 🔑 **Selenium Auto-Login:** Token ve UserID bilgilerini otomatik olarak çerezlerden yakalar.
* 🛡️ **Akıllı Failover:** Bir bölge sunucusu hata verirse, bot anında yedek bölgeye zıplar.

---

## 🛠️ Kurulum

1.  Python 3.10 veya üzeri bir sürümün yüklü olduğundan emin olun.
2.  Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install PyQt5 urllib3 selenium ntplib pytz webdriver-manager
    ```
3.  Uygulamayı çalıştırın:
    ```bash
    python hyperosunlocker_gui.py
    ```

---

## 📖 Kullanım Kılavuzu

1.  **Token Al:** Uygulamayı açın ve "Otomatik Token Al" butonuna tıklayın. Açılan Chrome penceresinde Xiaomi hesabınıza giriş yapın.
2.  **Ayarlar:** * **Thread Sayısı:** İnternet hızınıza göre 10-20 arası önerilir.
    * **Feedtime (ms):** İnternet pinginize göre 400ms - 500ms arası idealdir.
3.  **Başlat:** Saat 18:59:45 civarında "Sistemi Başlat" butonuna basın.
4.  **İzle:** Log ekranından sunucu yanıtlarını ve milisaniyeleri takip edin.

---

## ⚠️ Feragatname (Disclaimer)

Bu araç tamamen eğitim amaçlı ve Xiaomi'nin resmi başvuru sistemini kolaylaştırmak için yapılmıştır. Hesabınızın başvuru kriterlerini (30 günlük hesap, topluluk puanı vb.) karşılaması gerekir. Aracın kullanımıyla ilgili sorumluluk kullanıcıya aittir.

---

## 🤝 Katkıda Bulunma

Hataları bildirmek veya yeni özellikler eklemek için bir `Issue` açabilir veya `Pull Request` gönderebilirsiniz. 

**Main Repository:** [pwnj/auto-hyperos-unlocker](https://github.com/pwnj/auto-hyperos-unlocker)

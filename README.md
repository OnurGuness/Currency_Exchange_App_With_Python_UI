# 💰 Kur Radarı Pro v4 (CurrencyMaster)

**Her Güne Bir Proje Serisi - Gün X**

Bu proje, Python'ın güçlü arayüz kütüphanesi **CustomTkinter (ctk)** kullanılarak geliştirilmiş, canlı döviz kurlarını anlık olarak takip etmenizi sağlayan modern ve işlevsel bir masaüstü uygulamasıdır. `exchangerate-api.com` servisini kullanarak verileri çeker.

## ✨ Temel Özellikler

* **Canlı Veri Çekimi:** İnternet üzerinden güncel döviz kurlarını (TRY bazlı) asenkron (threading) olarak çeker.
* **Modern Arayüz (CustomTkinter):** Şık, karanlık temalı ve modern bir kullanıcı deneyimi sunar.
* **Mini Mod:** Uygulamayı ekranın üstünde kalabilen (topmost), kompakt ve sadece favori kurları gösteren bir **"Mini Moda"** geçirerek anlık takip imkanı sunar.
* **Favori Sistemi:** İstediğiniz döviz birimlerini favorilerinize ekleyip listenin en üstünde görebilirsiniz.
* **Arama ve Filtreleme:** Anlık arama çubuğu ile istediğiniz kuru kolayca bulun.
* **Görselleştirme:** Kur değerlerini görselleştiren (küçük, orta, yüksek) renkli bir ilerleme çubuğu (Progress Bar) mevcuttur (Normal Modda).

## 🛠️ Kurulum ve Çalıştırma

### Ön Gereksinimler

* Python 3.x
* CustomTkinter
* Requests

### Adımlar

1.  Projeyi klonlayın veya `currency_exchange_app.py` dosyasını indirin.
2.  Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install customtkinter requests
    ```
3.  Uygulamayı çalıştırın:
    ```bash
    python currency_exchange_app.py
    ```

## 🖼️ Ekran Görüntüleri



## 💡 Nasıl Çalışır?

Uygulama, temel olarak Türkiye Lirası (TRY) üzerinden diğer döviz birimlerinin karşılığını hesaplar.

1.  Uygulama, `https://api.exchangerate-api.com/v4/latest/TRY` adresine istek gönderir.
2.  Gelen yanıtta kurlar `(1 TRY = X döviz)` formatında olduğu için, biz bunu `(1 döviz = Y TRY)` formatına çevirmek için her kuru $1 / \text{rate}$ işlemiyle tersine çeviriyoruz.
3.  Veri çekme işlemi **Threading** ile ana arayüz (UI) iş parçacığını (thread) bloklamadan gerçekleştirilir.
4.  Veriler çekildikten sonra, `update_ui_list` fonksiyonu favorileri listenin en üstüne alacak şekilde arayüzü yeniden çizer.

## 🤝 Katkıda Bulunma

Geri bildirimleriniz ve katkılarınız her zaman kabul edilir! Bir hata bulursanız veya yeni bir özellik önermek isterseniz, lütfen bir Issue açın veya Pull Request gönderin.

---
`@OnurGuness>` tarafından, **Her Güne Bir Proje** serisi için geliştirilmiştir.

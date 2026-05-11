# DeauthAttackDetector

[Scapy](https://scapy.net/) kütüphanesi kullanılarak geliştirilmiş, çevredeki Wi-Fi trafiğini izleyip deauthentication (deauth) saldırılarını gerçek zamanlı tespit eden hafif bir Python aracı.

## Nasıl Çalışır?

Deauth paketleri, bir cihaz ağdan ayrılırken gönderilen meşru 802.11 yönetim çerçeveleridir. Ancak saldırganlar bu paketleri taklit ederek hedef cihazları ağdan düşürebilir. Bu teknik, Wi-Fi saldırılarında yaygın olarak kullanılır.

Bu araç, monitor mode sayesinde kapsama alanındaki tüm Wi-Fi çerçevelerini dinler. Aynı MAC adresinden **5 saniye içinde 5 veya daha fazla deauth paketi** gelirse o adresi saldırgan olarak işaretler ve bir log dosyasına kaydeder.

## Gereksinimler

- Python 3.x
- Scapy
- **Monitor mode** destekleyen bir Wi-Fi adaptör

```bash
pip install scapy
```

## Kurulum

Wi-Fi adaptörünüzü monitor mode'a alın:

```bash
sudo airmon-ng start wlan1
```

Doğrulamak için:

```bash
iwconfig
```

Çıktıda `Mode:Monitor` yazıyor olmalı.

## Kullanım

1. `deauth_detector.py` dosyasında interface adını kendinize göre güncelleyin:

```python
interface = "wlan1"  # Monitor mode'daki adaptörünüzün adı
```

2. Scripti root yetkisiyle çalıştırın:

```bash
sudo python3 deauth_detector.py
```

Araç deauth paketlerini dinlemeye başlar. Tespit edilen saldırılar hem konsola yazdırılır hem de `attackerLog.txt` dosyasına kaydedilir.

## Tespit Mantığı

- Scapy'nin `sniff()` fonksiyonu ile tüm 802.11 çerçeveleri dinlenir
- `Dot11Deauth` çerçeveleri filtrelenir
- Her kaynak MAC adresi için son 5 paketin timestamp'i tutulur
- Aynı MAC'ten 5 saniye içinde 5 paket gelirse saldırı uyarısı tetiklenir
- Aynı saldırgan için 60 saniye boyunca tekrar uyarı üretilmez
- Kaynak MAC, hedef MAC, zaman damgası, frame hızı ve reason code loglanır

## Örnek Çıktı

```
[*] Suspicious deauth activity detected from AA:BB:CC:DD:EE:FF targeting 11:22:33:44:55:66 at Mon May 11 14:32:01 2026 frame speed:1 reason code:7
```

## ⚠️ Yasal Uyarı

Bu araç yalnızca eğitim amaçlı ve yetkili ağ testleri için geliştirilmiştir. **Yalnızca kendi ağınızda veya açık izin aldığınız ortamlarda kullanın.**

# İşletim ve sürüm doğrulama — Türkçe finans metni çıkarımı

Son inceleme: **16 Ekim 2026**. Bu belge kurulum, veri akışı, sürüm kapıları, geri dönüş ve doğrulama kapsamını birlikte kaydeder. Bir yayın adresinin açılması, tüm üretim koşullarının tamamlandığı anlamına gelmez.

## Sürüm kanıtı

- Denetlenen uygulama commit’i: `89fe97e11eca3392bf550258c12b037e9b575510`.
- [Bu commit için başarılı CI kaydı](https://github.com/busrabuseucar/turkish-financial-information-extractor/actions/runs/38893811409).
- Doğrulanan otomatik kapsam: 35 Python testi.
- Testlerin gerçek servis, veri veya donanım yerine taklit kullandığı noktalar aşağıda açıkça ayrılmıştır.

## Kurulum ve çalışma

Depo kökünde, README’deki çalışma zamanı sürümüyle:

```sh
python -m pip install -c constraints-py312.txt -e ".[api,demo,test]"
python -m pytest -q
python scripts/evaluate.py --output evaluation.json
```

Veri akışı: Metin → kural tabanlı çıkarım → Decimal/takvim normalizasyonu → kaynak konumlu JSON.

Yapılandırma: Python 3.10/3.12; çekirdek API anahtarı veya model ağırlığı gerektirmez. API/Streamlit yerel geliştirme arayüzleridir.

## Yayın ve geri dönüş

1. Temiz checkout ve kilitli bağımlılıklarla yukarıdaki kontrolleri çalıştır. İlgili CI başarısını commit SHA ile eşleştir.
2. Yayın paketine yalnızca çalışma zamanı dosyalarını koy. Secret, ham kullanıcı verisi, yerel veritabanı ve kişisel hazırlık notları pakete girmemeli.
3. Hedef proje, kaynak commit, ortam ve yayın sürümünü kaydet. Önceki çalışan sürüm kimliğini geri dönüş için koru.
4. Yayından sonra ana kullanıcı akışını, hata durumunu ve varsa kalıcılığı doğrula. Sunucu hatası/yanlış sonuçta yeni yazmaları durdur; önceki doğrulanmış yayını geri al.
5. Şema değiştiyse yalnızca kodu geri almak yeterli değildir. Yedekten ayrı ortamda doğrulama yapmadan canlı veri üzerine yazma.

## Veri saklama ve kurtarma

Çekirdek metin saklamaz. JSON çıktısını ham kaynak metinle birlikte güvenli ortamda kullanıcı saklar; uygulamanın merkezi yedek deposu yok.

## Gerçek servis, model ve cihaz doğrulaması

30 sentetik örnekte micro F1=0.9747; bağımsız saha verisi değildir. Çoklu ürün, olumsuzluk ve hedef-kitle normalizasyon sınırları README’de belirtilmiştir. İnternete açık servis için kimlik doğrulama/kota gerekir.

## Yayın sonrası gözlem

Önce küçük ve sentetik girdilerle temel akışı kontrol et. Beklenmeyen hata, boş ekran, yanlış hesap, yetkisiz erişim veya veri kaybında tarih, uygulama commit’i, ortam ve yeniden üretme adımlarını kaydet; kişisel veri ve secret ekleme. Statik araçlarda tarayıcı konsolu/ağ hatalarını; backend bulunan projelerde durum kodu, gecikme ve hata oranını incele. Bu belgede sürekli izleme veya otomatik geri dönüş kurulmuş olduğu iddia edilmez.

## Kabul kaydı

Her yeni sürümün kaydı; test komutu/sonucu, kaynak SHA, yayın sürümü, gerçek servis/model sürümü, cihaz/işletim sistemi, veri kümesi özeti ve geri dönüş denemesini içermeli. Erişim veya fiziksel donanım yoksa ilgili satır **çalıştırılmadı** olarak tutulur; otomatik test başarısı yerine geçirilmez.

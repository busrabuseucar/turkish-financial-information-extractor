# Turkish Financial Information Extractor

Türkçe finansal ürün metinlerini kaynak kanıtıyla yapılandırılmış JSON'a dönüştüren Python projesi. Finansman tutarı, kâr payı/faiz oranı, vade, ücret, hedef kitle, ürün adı ve kampanya tarihi için kural tabanlı çıkarım yapar.

Her bulunan alan normalize değer, özgün metin, başlangıç/bitiş konumu ve sezgisel güven puanı içerir. Desteklenen kurallarla bulunamayan veya çelişen alanlar null döner. Çekirdek harici servis çağırmaz; API anahtarı gerekmez.

## Kurulum

Python 3.10 veya üzeri:

~~~bash
git clone https://github.com/busrabuseucar/turkish-financial-information-extractor.git
cd turkish-financial-information-extractor
python -m venv .venv
~~~

Linux/macOS: source .venv/bin/activate

Windows PowerShell: .venv\Scripts\Activate.ps1

~~~bash
python -m pip install -e ".[api,demo,test]"
~~~

Yalnızca çıkarıcı ve CLI için python -m pip install -e . yeterlidir. requirements.txt tam geliştirme kurulumunun kısa yoludur. Python 3.12/Linux doğrulamasında kullanılan sürümler constraints-py312.txt içindedir; aynı ortamda kurmak için:

~~~bash
python -m pip install -c constraints-py312.txt -e ".[api,demo,test]"
~~~

## Kullanım

~~~bash
turfinextract "120 ay vadeli ve %3,19 kâr payı oranlı finansman"
~~~

~~~python
from turfinextract import FinancialInformationExtractor

record = FinancialInformationExtractor().extract(
    "Tahsis ücreti 2.500 TL, finansman limiti 200.000 TL."
)
print(record.to_dict())
~~~

Bu örnekte fee değeri 2500, financing_amount değeri 200000 olur. Tam bir giriş ve gerçek CLI çıktısı examples/sample.txt ve examples/sample_output.json dosyalarındadır.

## Arayüzler

Komutları depo kökünde çalıştır:

~~~bash
python -m uvicorn app.api:app --reload
~~~

API dokümantasyonu: http://127.0.0.1:8000/docs

GET /health sağlık kontrolü; POST /extract gövdesi: {"text": "120 ay vadeli finansman"}.

~~~bash
python -m streamlit run app/streamlit_app.py
~~~

Streamlit metin girişi, kanıt tablosu ve JSON indirme sunar. API ve demo yerel geliştirme içindir; internete açık servis için kimlik doğrulama ve hız sınırlama ayrıca gerekir.

## Veri sözleşmesi

| Alan | Normalize değer örneği |
|---|---|
| product_name | Bereket Konut Finansmanı |
| financing_amount | 2500000 |
| profit_rate | %3.19 |
| maturity | 120 month |
| fee | 5000 |
| target_audience | yeni müşterilere |
| campaign_period | 2026-12-31 |

Değerler string olarak döner. start dahil, end hariç Python karakter indeksidir; text[start:end] kaynak metinle eşleşir. Para için Decimal, tarihler için takvim doğrulaması kullanılır. Girdi sınırı 20.000 karakterdir. Güven puanı ölçülmüş doğruluk olasılığı değildir.

## Doğrulama

~~~bash
python -m pytest -q
python scripts/evaluate.py --output evaluation.json
~~~

Python 3.12 temiz sanal ortamında **35 test geçti**: çıkarım/normalizasyon, kanıt konumları, eksik/çelişkili girdiler, API–CLI tutarlılığı, hatalı istekler ve Streamlit çıkarım akışı. CI dosyası Python 3.10 ve 3.12 üzerinde test, değerlendirme ve kurulabilir wheel kontrolü çalıştırır.

30 örneklik orijinal **sentetik geliştirme verisinde** tam alan değeri eşleştirmesiyle micro precision/recall/F1: **0.9747**. İki uyuşmazlık hedef kitle değerinin büyük/küçük harf farkıdır. Veri kümesinde pozitif ürün adı örneği yoktur; bu alanın başarısı bu veriyle ölçülmüş değildir. Tüm sayımlar ve uyuşmazlıklar [evaluation.json](evaluation.json) içindedir. Bu sonuç bağımsız test veya üretim doğruluğu iddiası değildir.

## Kapsam ve sınırlar

Tek ürün metni varsayılır. Tüm Türkçe ifadeler, olumsuzluklar, tarih aralıkları ve çoklu ürün karşılaştırmaları desteklenmez. Ücret bağlamı dışındaki para değerleri finansman adayı sayılır; gelir/bakiye ayrımı yapılmaz. Tek bir tarih çıkarılması, tarihin mutlaka kampanya bitişi olduğunu garanti etmez. Kritik değerler kaynak metinden doğrulanmalıdır.

- [Teknik Tasarım ve Kararlar](docs/TECHNICAL_DESIGN.md)
- [Dosya düzeni onarım kaydı](docs/RECOVERY.md)

Sonraki adımlar: bağımsız etiketli veri, olumsuzluk/çoklu ürün çözümleme, alan bazlı hata nedenleri ve güven puanı kalibrasyonu.

## Lisans

MIT — [LICENSE](LICENSE).

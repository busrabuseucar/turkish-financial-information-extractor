# Teknik anlatım ve kararlar

Türkçe finansal kampanya metnindeki yedi alanı kaynak metindeki konumlarıyla JSON'a dönüştüren deterministik bir çıkarıcı. Çekirdek Python paketi harici servis veya model çağırmaz. CLI, FastAPI ve Streamlit aynı çıkarıcıyı kullanır.

## Akış

1. Boş metni ve 20.000 karakteri aşan girdiyi reddet.
2. Alanlara özel regex kurallarıyla adayları bul.
3. Para adayını bitişik ücret/masraf bağlamına göre sınıflandır.
4. Sayıyı Decimal, tarihi gerçek takvim doğrulamasıyla normalize et.
5. Aynı alan için farklı normalize değerler varsa null döndür.
6. Kaynak dilimi ve karakter aralığını değerle birlikte döndür.

text[start:end] == source_text sözleşmesi test edilir. Konumlar Python Unicode karakter indeksidir; JavaScript UTF-16 indeksleriyle emoji içeren metinlerde doğrudan aynı olmayabilir.

## Kararlar

- Kurallar küçük kapsamda izlenebilir ve tekrar üretilebilir; dil çeşitliliği arttıkça bakım maliyeti yükselir.
- Decimal para değerlerinde ikili kayan nokta yuvarlamasını önler.
- null, desteklenen kurallarla bulunamayan veya çelişen değerler içindir. “Belirtilmemiş” ile “çelişkili” şu an ayrı hata türleri değildir.
- Ortak çekirdek API, CLI ve demo arasında davranış farkını azaltır.
- Sabit güven puanları kurala atanmış sezgisel değerlerdir; olasılık veya ölçülmüş doğruluk değildir.

## Örnekler

- “Tahsis ücreti 2.500 TL” → fee=2500, financing_amount=null.
- “100.000 TL kredi ve 200.000 TL kredi” → financing_amount=null.
- “31.02.2026” → campaign_period=null; geçerli takvim tarihi değildir.
- “%25 indirim” → profit_rate=null; faiz/kâr payı bağlamı yoktur.

## Sınırlar

Bir metinde tek ürün varsayılır. Çoklu ürün, tarih aralığı, olumsuzluk (“ücretsiz değildir”), uzak cümle ilişkileri, tüm olası ücret ifadeleri ve bütün Türkçe yazım biçimleri desteklenmez. Ücret dışındaki tutarlar finansman adayı kabul edilir; bakiye/gelir/ödeme ayrımı yapılmaz. Tek tarih bulunması onun mutlaka kampanya bitişi olduğunu kanıtlamaz. İnsan doğrulaması gerekir.

30 örnek orijinal sentetik geliştirme verisidir; bağımsız test kümesi veya üretim başarısı değildir. Sonraki adım, kaynağı ve etiketleme yöntemi kayıtlı bağımsız bir veri kümesiyle hata türlerini ölçmektir. API yerel demo içindir; kimlik doğrulama ve istek hız sınırı içermez.

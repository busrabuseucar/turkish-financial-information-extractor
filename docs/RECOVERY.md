# Dosya düzeninin onarımı

Önceki sürümde bazı Python modülleri paket metadata adlarıyla, veri ve arayüzler ise farklı modül adlarıyla kaydedilmişti.

| Eski dosya | Yeni konum |
|---|---|
| SOURCES.txt | src/turfinextract/extractor.py |
| dependency_links.txt | src/turfinextract/__init__.py |
| entry_points.txt | src/turfinextract/models.py |
| top_level.txt | src/turfinextract/normalization.py |
| test_extractor.py | src/turfinextract/cli.py |
| streamlit_app.py | app/api.py |
| __init__.py | app/streamlit_app.py |
| extractor.py | scripts/evaluate.py |
| sample_output.json | data/benchmark.jsonl |
| __init__ (1).py | examples/sample.txt |

Çıkarım, normalizasyon, CLI ve değerlendirme modülleri onarım sırasında güncellendi. Boş benchmark dosyası, yinelenen README kopyası ve eski kısmi çıktı kaldırıldı. Yeni örnek çıktı çalışan CLI'dan üretilir.

30 satırlık JSONL veri dosyasının içeriği değiştirilmedi. Önceki commit'teki sample_output.json ile SHA-256 özeti aynıdır; güncel özet evaluation.json içinde bulunur. Değerlendirme etiketleri sonuçlara uydurulmadı; uyuşmazlıklar raporda görünür.

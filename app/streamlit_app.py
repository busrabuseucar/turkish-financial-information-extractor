import json
import streamlit as st

from turfinextract import FinancialInformationExtractor

st.set_page_config(page_title="Turkish Financial Information Extractor", layout="wide")
st.title("Turkish Financial Information Extractor")
st.caption("Kanıt bağlantılı, kural tabanlı Türkçe finansal bilgi çıkarımı")
st.info("Tek bir ürün metni gir. Eksik, geçersiz veya çelişkili alanlar null döner. Güven puanları ölçülmüş doğruluk oranı değildir.")

sample = (
    "Bereket Konut Finansmanı kampanyası kapsamında yeni müşterilere "
    "2.500.000 TL'ye kadar, 120 ay vadeli ve %3,19 kâr payı oranlı finansman sunulmaktadır. "
    "Tahsis ücreti 5.000 TL'dir. Kampanya 31.12.2026 tarihine kadar geçerlidir."
)
text = st.text_area("Turkish financial text", value=sample, height=180, max_chars=20000)

if st.button("Extract", type="primary"):
    if not text.strip():
        st.error("Text cannot be empty.")
    else:
        result = FinancialInformationExtractor().extract(text).to_dict()
        left, right = st.columns([1, 1])
        with left:
            st.subheader("Structured output")
            st.json(result)
        with right:
            st.subheader("Evidence table")
            rows = []
            for field, evidence in result.items():
                rows.append({
                    "field": field,
                    "value": evidence["value"] if evidence else None,
                    "source_text": evidence["source_text"] if evidence else None,
                    "confidence": evidence["confidence"] if evidence else None,
                })
            st.dataframe(rows, use_container_width=True)
        st.download_button(
            "Download JSON",
            json.dumps(result, ensure_ascii=False, indent=2),
            file_name="extraction.json",
            mime="application/json",
        )

import streamlit as st
import feedparser

st.set_page_config(page_title="SciFeed", page_icon="🔬", layout="centered")

st.title("🔬 SciFeed")
st.subheader("Veille scientifique simple")

domaines = {
    "Physique Quantique": "https://arxiv.org/rss/quant-ph",
    "Biologie & Neurosciences": "https://arxiv.org/rss/q-bio",
    "Informatique & IA": "https://arxiv.org/rss/cs",
    "Hardware & Technologie": "https://arxiv.org/rss/physics",
    "Spiritualité & Science": "https://arxiv.org/rss/physics"
}

domaine = st.selectbox("Choisis un domaine :", list(domaines.keys()))

if st.button("🔄 Charger les études"):
    with st.spinner("Chargement..."):
        feed = feedparser.parse(domaines[domaine])
        entries = feed.entries[:8]
        
        for entry in entries:
            with st.expander("📌 Étude récente"):
                summary = (entry.summary[:600] + "...") if hasattr(entry, 'summary') else "Résumé non disponible."
                st.write(summary)
                st.caption("Publié récemment")
                if hasattr(entry, 'link'):
                    st.link_button("Lire l'article original", entry.link)

st.caption("SciFeed • Simple")

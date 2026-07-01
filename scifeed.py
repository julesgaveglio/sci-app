import streamlit as st
import feedparser
from datetime import datetime

st.set_page_config(page_title="SciFeed", page_icon="🔬", layout="centered")

st.title("🔬 SciFeed")
st.subheader("Veille scientifique simple")

domaines = {
    "Physique Quantique": "https://arxiv.org/rss/quant-ph",
    "Biologie & Neurosciences": "https://arxiv.org/rss/q-bio",
    "Informatique & IA": "https://arxiv.org/rss/cs",
    "Hardware & Technologie": "https://arxiv.org/rss/physics",
    "Spiritualité & Science": "https://arxiv.org/rss/physics"  # à ajuster
}

domaine = st.selectbox("Choisis ton domaine :", list(domaines.keys()))

if st.button("🔄 Charger les dernières études"):
    with st.spinner("Chargement via RSS..."):
        try:
            feed = feedparser.parse(domaines[domaine])
            entries = feed.entries[:6]
            
            if not entries:
                st.warning("Aucun article trouvé.")
            else:
                st.success(f"{len(entries)} articles récents")
                for entry in entries:
                    with st.expander(entry.title[:120] + "..." if len(entry.title) > 120 else entry.title):
                        st.caption(f"Publié le : {entry.published[:16] if 'published' in entry else 'Date inconnue'}")
                        summary = entry.summary[:500] + "..." if 'summary' in entry and len(entry.summary) > 500 else entry.get('summary', 'Pas de résumé disponible.')
                        st.write(summary)
                        if 'link' in entry:
                            st.link_button("Lire sur arXiv", entry.link)
        except:
            st.error("Impossible de charger pour le moment. Réessaie dans 1 minute.")

st.divider()
st.caption("SciFeed • Utilise les flux RSS d'arXiv")

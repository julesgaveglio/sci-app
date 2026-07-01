import streamlit as st
import feedparser

st.set_page_config(page_title="SciFeed", page_icon="🔬", layout="centered")

st.title("🔬 SciFeed")
st.subheader("Veille scientifique simple")

st.write("Choisis un domaine :")

domaines = {
    "Physique Quantique": "https://arxiv.org/rss/quant-ph",
    "Biologie & Neurosciences": "https://arxiv.org/rss/q-bio",
    "Informatique & IA": "https://arxiv.org/rss/cs",
    "Hardware & Technologie": "https://arxiv.org/rss/physics",
    "Spiritualité & Science": "https://arxiv.org/rss/physics"
}

domaine = st.selectbox("", list(domaines.keys()))

if st.button("🔄 Charger les dernières études", type="primary"):
    with st.spinner("Chargement..."):
        try:
            feed = feedparser.parse(domaines[domaine])
            entries = feed.entries[:8]
            
            if not entries:
                st.warning("Aucun article trouvé.")
            else:
                st.success(f"{len(entries)} études récentes")
                
                for entry in entries:
                    with st.expander("Article récent"):
                        # Résumé ultra-simple (première phrase + simplification)
                        summary = entry.summary if hasattr(entry, 'summary') else ""
                        simple_summary = summary.split('. ')[0] + "." if '.' in summary else summary[:300]
                        
                        st.write(f"**Cet article sert à :** {simple_summary}")
                        st.caption(f"Publié le : {entry.published[:16] if hasattr(entry, 'published') else 'Date inconnue'}")
                        
                        if hasattr(entry, 'link'):
                            st.link_button("Voir l'article complet", entry.link)
        except:
            st.error("Impossible de charger pour le moment. Réessaie dans 30 secondes.")

st.divider()
st.caption("SciFeed • Tout en français • Simple et clair")

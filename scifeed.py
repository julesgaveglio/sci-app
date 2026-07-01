import streamlit as st
import feedparser

st.set_page_config(page_title="SciFeed", page_icon="🔬", layout="centered")

st.title("🔬 SciFeed")
st.subheader("Veille scientifique simple - Résumés clairs")

st.write("Choisis un domaine pour voir les dernières études :")

domaines = {
    "Physique Quantique": "https://arxiv.org/rss/quant-ph",
    "Biologie & Neurosciences": "https://arxiv.org/rss/q-bio",
    "Informatique & IA": "https://arxiv.org/rss/cs",
    "Hardware & Technologie": "https://arxiv.org/rss/physics",
    "Spiritualité & Science": "https://arxiv.org/rss/physics"  
}

domaine = st.selectbox("", list(domaines.keys()))

if st.button("🔄 Charger les dernières études", type="primary"):
    with st.spinner("Chargement des articles..."):
        try:
            feed = feedparser.parse(domaines[domaine])
            entries = feed.entries[:8]
            
            if not entries:
                st.warning("Aucun article trouvé pour le moment.")
            else:
                st.success(f"{len(entries)} articles récents trouvés")
                
                for entry in entries:
                    with st.expander(entry.title[:140] + "..." if len(entry.title) > 140 else entry.title):
                        date = entry.published[:16] if hasattr(entry, 'published') else "Date inconnue"
                        st.caption(f"**Publié le :** {date}")
                        
                        summary = entry.summary[:550] + "..." if hasattr(entry, 'summary') and len(entry.summary) > 550 else entry.get('summary', "Pas de résumé disponible.")
                        st.write(summary)
                        
                        if hasattr(entry, 'link'):
                            st.link_button("📄 Aller sur l'article officiel", entry.link)
        except:
            st.error("Impossible de charger les données pour le moment. Réessaie dans une minute.")

st.divider()
st.caption("SciFeed • Application simple par Grok")

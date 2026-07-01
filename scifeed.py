import streamlit as st
import arxiv
import time
from datetime import datetime

st.set_page_config(page_title="SciFeed", page_icon="🔬", layout="centered")

st.title("🔬 SciFeed")
st.subheader("Résumés ultra-simples de la recherche")

domaines = {
    "Physique Quantique": "quant-ph",
    "Biologie & Neurosciences": "neuroscience OR biophysics",
    "Informatique & IA": "machine learning OR artificial intelligence",
    "Hardware & Technologie": "nanotechnology OR semiconductor",
    "Spiritualité & Science": "consciousness OR meditation"
}

domaine = st.selectbox("Choisis ton domaine :", list(domaines.keys()))

if st.button("🔄 Charger les dernières études", type="primary"):
    with st.spinner("Connexion à arXiv..."):
        try:
            time.sleep(1)  # Petit délai pour éviter le rate limit
            search = arxiv.Search(
                query=domaines[domaine],
                max_results=6,
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending
            )
            papers = list(search.results())
            
            st.success(f"{len(papers)} articles trouvés")
            
            for paper in papers:
                with st.expander(f"📝 {paper.title[:100]}..." if len(paper.title) > 100 else paper.title):
                    st.caption(f"**Publié le :** {paper.published.strftime('%d %B %Y')}")
                    summary = paper.summary[:520] + "..." if len(paper.summary) > 520 else paper.summary
                    st.write(summary)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.link_button("📄 PDF", paper.pdf_url)
                    with col2:
                        st.link_button("🌐 Page complète", paper.entry_id)
                        
        except Exception as e:
            st.error("arXiv est temporairement lent. Réessaie dans 20 secondes.")
            st.info("C'est fréquent sur arXiv, patience...")

st.divider()
st.caption("SciFeed - Veille scientifique simple")

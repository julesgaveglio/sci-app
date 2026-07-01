import streamlit as st
import arxiv
from datetime import datetime

st.set_page_config(page_title="SciFeed", page_icon="🔬", layout="centered")

st.title("🔬 SciFeed")
st.subheader("Résumés ultra-simples")

domaines = {
    "Physique Quantique": "quant-ph",
    "Biologie & Neurosciences": "neuroscience OR biophysics",
    "Informatique & IA": "machine learning OR artificial intelligence",
    "Hardware & Technologie": "nanotechnology OR semiconductor OR hardware",
    "Spiritualité & Science": "consciousness OR meditation science"
}

domaine = st.selectbox("Choisis ton domaine :", list(domaines.keys()))

if st.button("🔄 Charger les dernières études", type="primary"):
    with st.spinner("Recherche en cours..."):
        try:
            search = arxiv.Search(
                query=domaines[domaine],
                max_results=8,
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending
            )
            papers = list(search.results())
            
            if not papers:
                st.warning("Aucun article trouvé pour le moment.")
            else:
                for paper in papers:
                    with st.expander(f"📝 {paper.title[:110]}{'...' if len(paper.title) > 110 else ''}"):
                        st.caption(f"**Date :** {paper.published.strftime('%d %B %Y')}")
                        summary = paper.summary[:480] + "..." if len(paper.summary) > 480 else paper.summary
                        st.write(summary)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("📄 PDF", key=paper.entry_id):
                                st.link_button("Ouvrir PDF", paper.pdf_url)
                        with col2:
                            st.link_button("🌐 arXiv", paper.entry_id)
        except Exception as e:
            st.error("Erreur de connexion à arXiv. Réessaie dans quelques secondes.")

st.divider()
st.caption("SciFeed • Simple & Rapide")

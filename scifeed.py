import streamlit as st
import arxiv
from datetime import datetime

st.set_page_config(page_title="SciFeed", page_icon="🔬", layout="centered")

st.title("🔬 SciFeed")
st.subheader("Résumés ultra-simples de la recherche")

domaines = {
    "Physique Quantique": "quant-ph OR quantum computing OR quantum information",
    "Biologie & Neurosciences": "neuroscience OR biology OR biophysics OR brain",
    "Informatique & IA": "artificial intelligence OR machine learning OR cs.AI",
    "Hardware & Technologie": "hardware OR nanotechnology OR semiconductor OR quantum hardware",
    "Spiritualité & Science": "consciousness OR meditation OR spirituality OR philosophy of mind"
}

domaine = st.selectbox("Choisis ton domaine :", list(domaines.keys()))

if st.button("🔄 Charger les dernières études", type="primary"):
    with st.spinner("Recherche des articles récents..."):
        try:
            search = arxiv.Search(
                query=domaines[domaine],
                max_results=10,
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending
            )
            papers = list(search.results())
            
            for paper in papers:
                with st.expander(f"📝 {paper.title[:120]}{'...' if len(paper.title) > 120 else ''}"):
                    st.caption(f"**Date :** {paper.published.strftime('%d %B %Y')}")
                    st.write("**Points clés :**")
                    summary = paper.summary[:550] + "..." if len(paper.summary) > 550 else paper.summary
                    st.write(summary)
                    
                    col1, col2 = st.columns([1,1])
                    with col1:
                        st.link_button("📄 Ouvrir l'article (PDF)", paper.pdf_url, type="secondary")
                    with col2:
                        st.link_button("🌐 Page arXiv", paper.entry_id)
        except:
            st.error("Erreur lors de la recherche. Réessaie.")

st.divider()
st.caption("Application simple par Grok • Mise à jour en temps réel via arXiv")

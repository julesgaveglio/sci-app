import streamlit as st
import arxiv
import time

st.set_page_config(page_title="SciFeed", page_icon="🔬", layout="centered")

st.title("🔬 SciFeed")
st.subheader("Résumés ultra-simples")

domaines = {
    "Physique Quantique": "quant-ph",
    "Biologie & Neurosciences": "neuroscience OR brain",
    "Informatique & IA": "machine learning OR artificial intelligence",
    "Hardware & Technologie": "nanotechnology OR semiconductor",
    "Spiritualité & Science": "consciousness"
}

domaine = st.selectbox("Choisis ton domaine :", list(domaines.keys()))

if st.button("🔄 Charger les dernières études", type="primary"):
    with st.spinner("Connexion à arXiv (peut prendre 10-15 secondes)..."):
        time.sleep(2)   # Délai important
        try:
            search = arxiv.Search(
                query=domaines[domaine],
                max_results=5,
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending
            )
            papers = list(search.results())
            
            if papers:
                st.success(f"{len(papers)} articles trouvés")
                for paper in papers:
                    with st.expander(f"📝 {paper.title[:110]}..."):
                        st.caption(f"**Date :** {paper.published.strftime('%d %B %Y')}")
                        summary = paper.summary[:520] + "..." if len(paper.summary) > 520 else paper.summary
                        st.write(summary)
                        st.link_button("📄 PDF", paper.pdf_url)
                        st.link_button("🌐 arXiv", paper.entry_id)
            else:
                st.warning("Aucun article trouvé.")
        except:
            st.error("arXiv est lent. Attends 30 secondes et réessaie.")

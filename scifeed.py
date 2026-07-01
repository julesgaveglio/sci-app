import streamlit as st
import requests
import time

st.set_page_config(page_title="SciFeed", page_icon="🔬", layout="centered")

st.title("🔬 SciFeed")
st.subheader("Résumés ultra-simples")

domaines = {
    "Physique Quantique": "quantum physics",
    "Biologie & Neurosciences": "neuroscience",
    "Informatique & IA": "artificial intelligence",
    "Hardware & Technologie": "nanotechnology",
    "Spiritualité & Science": "consciousness science"
}

domaine = st.selectbox("Choisis ton domaine :", list(domaines.keys()))

if st.button("🔄 Charger les dernières études", type="primary"):
    with st.spinner("Recherche via Semantic Scholar..."):
        try:
            query = domaines[domaine]
            url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit=8&fields=title,authors,year,abstract,url,venue"
            
            response = requests.get(url, headers={"User-Agent": "SciFeedApp"})
            
            if response.status_code == 200:
                data = response.json()
                papers = data.get("data", [])
                
                if not papers:
                    st.warning("Aucun article trouvé.")
                else:
                    st.success(f"{len(papers)} articles trouvés")
                    for paper in papers:
                        with st.expander(f"📝 {paper['title'][:110]}..." if len(paper['title']) > 110 else paper['title']):
                            st.caption(f"**Année :** {paper.get('year', 'N/A')}")
                            abstract = paper.get('abstract', 'Pas de résumé disponible.')[:500]
                            st.write(abstract + "..." if len(abstract) == 500 else abstract)
                            
                            if paper.get('url'):
                                st.link_button("🌐 Voir sur Semantic Scholar", paper['url'])
            else:
                st.error(f"Erreur {response.status_code}")
        except:
            st.error("Problème de connexion. Réessaie.")

st.divider()
st.caption("SciFeed • Données via Semantic Scholar")

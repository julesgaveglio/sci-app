import streamlit as st
import requests
import time

st.set_page_config(page_title="SciFeed", page_icon="🔬", layout="centered")

st.title("🔬 SciFeed")
st.subheader("Résumés ultra-simples")

domaines = {
    "Physique Quantique": "quantum",
    "Biologie & Neurosciences": "neuroscience",
    "Informatique & IA": "machine learning",
    "Hardware & Technologie": "nanotechnology",
    "Spiritualité & Science": "consciousness"
}

domaine = st.selectbox("Choisis ton domaine :", list(domaines.keys()))

if st.button("🔄 Charger les dernières études", type="primary"):
    with st.spinner("Recherche en cours (patience)..."):
        try:
            query = domaines[domaine]
            url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit=5&fields=title,authors,year,abstract,url"
            
            headers = {"User-Agent": "SciFeed/1.0"}
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                papers = data.get("data", [])
                
                st.success(f"{len(papers)} articles trouvés")
                
                for i, paper in enumerate(papers):
                    with st.expander(f"{i+1}. {paper['title'][:100]}..."):
                        st.caption(f"**Année :** {paper.get('year', 'N/A')}")
                        abstract = paper.get('abstract') or "Résumé non disponible."
                        st.write(abstract[:550] + "..." if len(abstract) > 550 else abstract)
                        
                        if paper.get('url'):
                            st.link_button("🌐 Voir l'article", paper['url'])
            elif response.status_code == 429:
                st.error("Trop de requêtes. Attends 30 secondes puis réessaie.")
            else:
                st.error(f"Erreur {response.status_code}")
        except Exception as e:
            st.error("Erreur de connexion. Réessaie dans 20 secondes.")

st.divider()
st.caption("SciFeed • Simple veille scientifique")

import streamlit as st
import feedparser
import requests

st.set_page_config(page_title="SciFeed", page_icon="🔬", layout="centered")

st.title("🔬 SciFeed")
st.subheader("Veille scientifique - Résumés IA simples")

GROQ_API_KEY = "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"

domaines = {
    "Physique Quantique": "https://arxiv.org/rss/quant-ph",
    "Biologie & Neurosciences": "https://arxiv.org/rss/q-bio",
    "Informatique & IA": "https://arxiv.org/rss/cs",
    "Hardware & Technologie": "https://arxiv.org/rss/physics",
    "Spiritualité & Science": "https://arxiv.org/rss/physics"
}

domaine = st.selectbox("Choisis un domaine :", list(domaines.keys()))

if st.button("🔄 Charger + Résumé IA", type="primary"):
    with st.spinner("Analyse avec IA en cours..."):
        feed = feedparser.parse(domaines[domaine])
        entries = feed.entries[:6]
        
        for entry in entries:
            title = entry.title
            abstract = entry.summary[:700] if hasattr(entry, 'summary') else ""
            
            # Appel Groq
            try:
                resp = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
                    json={
                        "model": "llama3-8b-8192",
                        "messages": [{"role": "user", "content": f"Résume cet article en **une seule phrase très simple** en français. Dis clairement à quoi il sert :\n\nTitre: {title}\n\nContenu: {abstract}"}],
                        "temperature": 0.7,
                        "max_tokens": 120
                    },
                    timeout=15
                )
                
                if resp.status_code == 200:
                    summary = resp.json()["choices"][0]["message"]["content"].strip()
                else:
                    summary = "Résumé non disponible (erreur API)."
            except:
                summary = "Impossible de générer le résumé pour le moment."
            
            with st.expander("📌 Étude récente"):
                st.write(f"**Cet article sert à :** {summary}")
                st.caption(f"Domaine : {domaine}")
                if hasattr(entry, 'link'):
                    st.link_button("Lire l'article original", entry.link)
            
            st.divider()

st.caption("SciFeed • Résumés par IA Groq")

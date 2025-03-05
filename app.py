import streamlit as st
from functions import load_resources, get_recommendations, get_poster
import base64

st.set_page_config(
    page_title="Movie Recommender Pro",
    page_icon="🎬",
    layout="wide"
)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css("style.css")

@st.cache_resource
def load_all_resources():
    return load_resources()

df, vectorizer, tfidf_matrix = load_all_resources()

# Sidebar
with st.sidebar:
    st.title("🎛️ Pengaturan")
    theme = st.selectbox("Tema Tampilan", ["Terang", "Gelap"])
    st.markdown("---")
    st.info("""
    **Panduan Penggunaan:**
    1. Masukkan judul film atau kata kunci
    2. Tekan Enter untuk melihat rekomendasi
    3. Klik tombol Detail untuk informasi lengkap
    """)

# Tema 
st.markdown(f'<div class="{"dark-theme" if theme == "Gelap" else ""}">', unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-section">
    <h1>🍿 Movie Recommender Pro</h1>
    <p>Temukan film serupa berdasarkan preferensi Anda!</p>
</div>
""", unsafe_allow_html=True)

search_input = st.text_input("🔍 Masukkan judul film atau kata kunci:", key="search")

if search_input:
    with st.spinner('🔎 Mencari rekomendasi terbaik...'):
        recommendations = get_recommendations(df, vectorizer, tfidf_matrix, search_input)
        st.subheader(f"🎉 Hasil Rekomendasi untuk: '{search_input}'")
        cols = st.columns(4)
        for idx, (_, row) in enumerate(recommendations.iterrows()):
            with cols[idx % 4]:
                st.markdown(f"""
                <div class="movie-card">
                    <img src="https://image.tmdb.org/t/p/w500{row['poster_path']}" 
                         class="poster-image"
                         onerror="this.src='data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='">
                    <h3>{row['title']}</h3>
                    <div class="movie-info">
                        <p>🎭 {row['genres']}</p>
                        <p>⭐ {row['weighted_rating']:.1f}/10</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Detail 
                with st.expander(f"ℹ️ Detail Film - {row['title']}", expanded=False):
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.image(get_poster(row['poster_path']), use_column_width=True)
                    with col2:
                        st.markdown(f"""
                            **📅 Tahun Rilis:** `{row['release_date']}`  
                            **⏱ Durasi:** `{row['runtime']} menit`  
                            **💵 Budget:** `${row['budget']:,}`  
                            **💰 Pendapatan:** `${row['revenue']:,}`  
                            **🌍 Bahasa:** `{row['spoken_languages']}`  
                            **📝 Plot:** _{row['overview']}_  
                            **🏭 Produksi:** `{row['production_companies']}`  
                            **🏆 Rating:** `{row['weighted_rating']}`  
                            **🔞 Dewasa:** `{'Ya' if row['adult'] else 'Tidak'}`
                        """)
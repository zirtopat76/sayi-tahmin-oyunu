import streamlit as st
import random
import sys
import asyncio
import base64
import os

# --- Windows Hata Engelleme ---
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# --- Ses Çalma Yardımcı Fonksiyonu ---
def get_audio_html(file_path, autoplay=True, loop=False):
    """MP3 dosyasını HTML5 audio etiketi ile hazırlar."""
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            auto_str = "autoplay" if autoplay else ""
            loop_str = "loop" if loop else ""
            return f'<audio src="data:audio/mp3;base64,{b64}" {auto_str} {loop_str} style="display:none;"></audio>'
    return ""

# --- Sayfa Yapılandırması ---
st.set_page_config(
    page_title="🎯 Anime Sayı Tahmin",
    page_icon="☁️",
    layout="centered"
)

# --- CSS Tasarımı ---
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1518176219326-1e64903ed7bf?q=80&w=1920&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .block-container {
        background-color: rgba(255, 255, 255, 0.75);
        padding: 2rem;
        border-radius: 20px;
        backdrop-filter: blur(5px);
        margin-top: 30px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    h1, p {
        color: #2e6091 !important;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    .stNumberInput input {
        border-radius: 50px;
        border: 2px solid #5d9cec;
        padding: 10px;
        text-align: center;
        font-size: 1.2rem;
        width: 100px;
        font-weight: bold;
    }
    .stNumberInput label { display: none; }
    .stButton>button[kind="secondary"] {
        background-color: #5d9cec;
        color: white;
        font-size: 1.3rem;
        width: 45px;
        height: 45px;
        border-radius: 50px;
        border: none;
    }
    .stButton>button[kind="primary"] {
        background-color: #ffce54;
        color: #333;
        font-size: 1.5rem;
        width: 60px;
        height: 60px;
        border-radius: 50px;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- Oyun Mantığı ---
if 'hedef_sayi' not in st.session_state:
    st.session_state.hedef_sayi = random.randint(1, 100)
    st.session_state.tahmin_sayisi = 0
if 'current_guess' not in st.session_state:
    st.session_state.current_guess = 50

# --- Ses HTML Konteyneri ---
audio_placeholder = st.empty()

# Arka Plan Müziği Ekranı (Kullanıcı oynatabilsin diye)
if os.path.exists("gerilim.mp3"):
    with st.expander("🎵 Arka Plan Müziği (Aç / Kapa)"):
        st.audio("gerilim.mp3", format="audio/mp3", loop=True)

st.markdown("<h1 style='text-align: center;'>☁️ Sayı Tahmin Dünyası 🍭</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>1 ile 100 arası tuttuğum sayıyı bilebilecek misin?</p>", unsafe_allow_html=True)

cols = st.columns([1, 1.5, 1], gap="small")

with cols[0]:
    st.markdown('<div style="display:flex; flex-direction:column; gap:5px; align-items:flex-end; margin-top: 15px;">', unsafe_allow_html=True)
    btn_artir = st.button("+", key="btn_plus", type="secondary")
    btn_azalt = st.button("-", key="btn_minus", type="secondary")
    st.markdown('</div>', unsafe_allow_html=True)

    if btn_artir and st.session_state.current_guess < 100:
        st.session_state.current_guess += 1
    if btn_azalt and st.session_state.current_guess > 1:
        st.session_state.current_guess -= 1

with cols[1]:
    tahmin = st.number_input(
        "Tahmin:",
        min_value=1,
        max_value=100,
        value=st.session_state.current_guess,
        step=1,
        key="main_input"
    )
    st.session_state.current_guess = tahmin

with cols[2]:
    st.markdown('<div style="margin-top: 15px;">', unsafe_allow_html=True)
    btn_tahmin = st.button("😊", key="btn_check", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<hr style='border: 1px dashed #5d9cec;'>", unsafe_allow_html=True)

if btn_tahmin:
    st.session_state.tahmin_sayisi += 1
    current_tahmin = st.session_state.current_guess
    
    if current_tahmin < st.session_state.hedef_sayi:
        audio_placeholder.markdown(get_audio_html("yanlis.mp3"), unsafe_allow_html=True)
        st.warning(f"Cıkk! Daha BÜYÜK bir sayı söylemelisin! ⬆️ (Deneme: {st.session_state.tahmin_sayisi})")
    elif current_tahmin > st.session_state.hedef_sayi:
        audio_placeholder.markdown(get_audio_html("yanlis.mp3"), unsafe_allow_html=True)
        st.warning(f"Hımm! Daha KÜÇÜK bir sayı söylemelisin! ⬇️ (Deneme: {st.session_state.tahmin_sayisi})")
    else:
        audio_placeholder.markdown(get_audio_html("dogru.mp3"), unsafe_allow_html=True)
        st.success(f"🎉 TEBRİKLER! {st.session_state.tahmin_sayisi}. denemede bildin!")
        st.balloons()
        
        if st.button("Tekrar Oyna? 🌀"):
            st.session_state.hedef_sayi = random.randint(1, 100)
            st.session_state.tahmin_sayisi = 0
            st.session_state.current_guess = 50
            st.rerun()
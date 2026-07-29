import streamlit as st
import random
import sys
import asyncio
import os

# --- Windows Hata Engelleme ---
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

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
        background-color: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 20px;
        backdrop-filter: blur(5px);
        margin-top: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    h1, h2, h3, p {
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
    
    /* Buton Tasarımları */
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
    
    /* Aralık Bilgi Kutusu */
    .range-box {
        background-color: #e6f2ff;
        border: 2px dashed #5d9cec;
        border-radius: 15px;
        padding: 10px;
        text-align: center;
        font-weight: bold;
        color: #2e6091;
        margin: 15px 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- Oyun Mantığı Ve Hafıza (Session State) ---
if 'hedef_sayi' not in st.session_state:
    st.session_state.hedef_sayi = random.randint(1, 100)
    st.session_state.tahmin_sayisi = 0
    st.session_state.min_limit = 1
    st.session_state.max_limit = 100
    st.session_state.last_sound = None

if 'current_guess' not in st.session_state:
    st.session_state.current_guess = 50

# --- Arka Plan Müziği (Açılabilir Oynatıcı) ---
if os.path.exists("gerilim.mp3"):
    st.markdown("##### 🎵 Arka Plan Müziği")
    st.audio("gerilim.mp3", format="audio/mp3", loop=True)

# --- Ses Efektleri Tetikleyici ---
if st.session_state.last_sound == "yanlis" and os.path.exists("yanlis.mp3"):
    st.audio("yanlis.mp3", format="audio/mp3", autoplay=True)
    st.session_state.last_sound = None
elif st.session_state.last_sound == "dogru" and os.path.exists("dogru.mp3"):
    st.audio("dogru.mp3", format="audio/mp3", autoplay=True)
    st.session_state.last_sound = None

# --- Başlık ve Açıklama ---
st.markdown("<h1 style='text-align: center;'>☁️ Sayı Tahmin Dünyası 🍭</h1>", unsafe_allow_html=True)

# --- Dynamic Daralan Aralık Göstergesi (Özellik 3) ---
st.markdown(f"""
    <div class="range-box">
        🎯 Hedef Sayı Şu Aralıkta: <br>
        <span style="font-size: 1.4rem; color: #d9534f;">{st.session_state.min_limit}</span> 
        &nbsp; ➖ [ ❓ ] ➖ &nbsp; 
        <span style="font-size: 1.4rem; color: #d9534f;">{st.session_state.max_limit}</span>
    </div>
""", unsafe_allow_html=True)

# İlerleme çubuğu ile görselleştirme
progress_value = max(0.0, min(1.0, (st.session_state.max_limit - st.session_state.min_limit) / 100))
st.caption("🔍 Tahmin Aralığı Daralıyor:")
st.progress(1.0 - progress_value)


# --- Tahmin Input Alanı ---
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


# --- Tahmin Kontrolü ---
if btn_tahmin:
    st.session_state.tahmin_sayisi += 1
    current_tahmin = st.session_state.current_guess
    
    if current_tahmin < st.session_state.hedef_sayi:
        st.session_state.last_sound = "yanlis"
        # Minimum sınırı daralt
        if current_tahmin > st.session_state.min_limit:
            st.session_state.min_limit = current_tahmin
        st.warning(f"Cıkk! Daha BÜYÜK bir sayı söylemelisin! ⬆️ (Deneme: {st.session_state.tahmin_sayisi})")
        st.rerun()

    elif current_tahmin > st.session_state.hedef_sayi:
        st.session_state.last_sound = "yanlis"
        # Maksimum sınırı daralt
        if current_tahmin < st.session_state.max_limit:
            st.session_state.max_limit = current_tahmin
        st.warning(f"Hımm! Daha KÜÇÜK bir sayı söylemelisin! ⬇️ (Deneme: {st.session_state.tahmin_sayisi})")
        st.rerun()

    else:
        st.session_state.last_sound = "dogru"
        st.success(f"🎉 TEBRİKLER! {st.session_state.tahmin_sayisi}. denemede bildin! Sayı {st.session_state.hedef_sayi} idi ⭐")
        st.balloons()

# --- Tekrar Oyna / Yenile Butonu (Özellik 2) ---
st.write("")
if st.button("🌀 Tekrar Oyna (Yenile)"):
    st.session_state.hedef_sayi = random.randint(1, 100)
    st.session_state.tahmin_sayisi = 0
    st.session_state.min_limit = 1
    st.session_state.max_limit = 100
    st.session_state.current_guess = 50
    st.session_state.last_sound = None
    st.rerun()
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
    page_title="🎯 Sayı Tahmin Oyun",
    page_icon="☁️",
    layout="centered"
)

# --- CSS Tasarımı & Mobil Responsive Ayarları ---
st.markdown("""
    <style>
    /* Arka Plan */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1518176219326-1e64903ed7bf?q=80&w=1920&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Responsive Ana Konteyner */
    .block-container {
        background-color: rgba(255, 255, 255, 0.90);
        padding: 1.5rem !important;
        border-radius: 20px;
        backdrop-filter: blur(8px);
        margin-top: 15px;
        max-width: 500px !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    
    h1, h2, h3, p {
        color: #2e6091 !important;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        text-align: center;
    }

    /* Input Alanı Şekillendirme */
    .stTextInput input {
        border-radius: 12px !important;
        border: 2px solid #5d9cec !important;
        padding: 12px !important;
        text-align: center !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        color: #333 !important;
    }
    
    /* Input Etiketini Gizle */
    .stTextInput label { display: none; }

    /* Tahmin Et Butonu (Gülümseyen İfade) */
    div[data-testid="column"]:nth-child(2) button[kind="primary"] {
        background-color: #ffce54 !important;
        color: #333 !important;
        font-size: 1.5rem !important;
        width: 100% !important;
        height: 50px !important;
        border-radius: 12px !important;
        border: none !important;
    }

    /* Kare 'Tekrar Oyna' Butonu */
    .reset-btn button {
        background-color: #5d9cec !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 1rem !important;
        width: 100px !important;
        height: 100px !important;
        border-radius: 12px !important; /* Kare şeklinde hafif kavisli */
        border: none !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin: 0 auto;
        display: block;
    }
    
    .reset-btn button:hover {
        background-color: #4a89dc !important;
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

# --- Oyun Mantığı Ve Hafıza ---
if 'hedef_sayi' not in st.session_state:
    st.session_state.hedef_sayi = random.randint(1, 100)
    st.session_state.tahmin_sayisi = 0
    st.session_state.min_limit = 1
    st.session_state.max_limit = 100
    st.session_state.last_sound = None

# --- Arka Plan Müziği ---
if os.path.exists("gerilim.mp3"):
    st.markdown("<p style='font-size: 0.9rem;'>🎵 Arka Plan Müziği</p>", unsafe_allow_html=True)
    st.audio("gerilim.mp3", format="audio/mp3", loop=True)

# --- Ses Efektleri Tetikleyici ---
if st.session_state.last_sound == "yanlis" and os.path.exists("yanlis.mp3"):
    st.audio("yanlis.mp3", format="audio/mp3", autoplay=True)
    st.session_state.last_sound = None
elif st.session_state.last_sound == "dogru" and os.path.exists("dogru.mp3"):
    st.audio("dogru.mp3", format="audio/mp3", autoplay=True)
    st.session_state.last_sound = None

# --- Başlık ---
st.markdown("<h1>☁️ Sayı Tahmin Dünyası 🍭</h1>", unsafe_allow_html=True)

# --- Dinamik Daralan Aralık Göstergesi ---
st.markdown(f"""
    <div class="range-box">
        🎯 Hedef Sayı Şu Aralıkta: <br>
        <span style="font-size: 1.4rem; color: #d9534f;">{st.session_state.min_limit}</span> 
        &nbsp; ➖ [ ❓ ] ➖ &nbsp; 
        <span style="font-size: 1.4rem; color: #d9534f;">{st.session_state.max_limit}</span>
    </div>
""", unsafe_allow_html=True)

# İlerleme Çubuğu
progress_value = max(0.0, min(1.0, (st.session_state.max_limit - st.session_state.min_limit) / 100))
st.caption("🔍 Tahmin Aralığı Daralıyor:")
st.progress(1.0 - progress_value)

# --- Tahmin Alanı (Giriş Kutusu + Buton) ---
col_input, col_btn = st.columns([3, 1], gap="small")

with col_input:
    # Tıklandığında kaybolan "Guess" yazısı (placeholder)
    tahmin_input = st.text_input("Tahmin", placeholder="Guess", key="user_guess")

with col_btn:
    btn_tahmin = st.button("😊", key="btn_check", type="primary")

st.markdown("<hr style='border: 1px dashed #5d9cec; margin: 20px 0;'>", unsafe_allow_html=True)

# --- Tahmin Kontrolü ---
if btn_tahmin:
    if tahmin_input.isdigit():
        current_tahmin = int(tahmin_input)
        st.session_state.tahmin_sayisi += 1
        
        if current_tahmin < st.session_state.hedef_sayi:
            st.session_state.last_sound = "yanlis"
            if current_tahmin > st.session_state.min_limit:
                st.session_state.min_limit = current_tahmin
            st.warning(f"Cıkk! Daha BÜYÜK bir sayı söylemelisin! ⬆️ (Deneme: {st.session_state.tahmin_sayisi})")
            st.rerun()

        elif current_tahmin > st.session_state.hedef_sayi:
            st.session_state.last_sound = "yanlis"
            if current_tahmin < st.session_state.max_limit:
                st.session_state.max_limit = current_tahmin
            st.warning(f"Hımm! Daha KÜÇÜK bir sayı söylemelisin! ⬇️ (Deneme: {st.session_state.tahmin_sayisi})")
            st.rerun()

        else:
            st.session_state.last_sound = "dogru"
            st.success(f"🎉 TEBRİKLER! {st.session_state.tahmin_sayisi}. denemede bildin! Sayı {st.session_state.hedef_sayi} idi ⭐")
            st.balloons()
    else:
        st.error("Lütfen geçerli bir sayı girin!")

# --- Kare Tekrar Oyna Butonu ---
st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
if st.button("Tekrar\nOyna", key="reset_game"):
    st.session_state.hedef_sayi = random.randint(1, 100)
    st.session_state.tahmin_sayisi = 0
    st.session_state.min_limit = 1
    st.session_state.max_limit = 100
    st.session_state.last_sound = None
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
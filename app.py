import streamlit as st
import random
import sys
import asyncio

# --- Windows Hata Engelleme (Önceki adımdan) ---
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# --- Sayfa Yapılandırması ---
st.set_page_config(
    page_title="🎯 Anime Sayı Tahmin",
    page_icon="☁️",
    layout="centered"
)

# --- CSS ile Arka Plan ve Görüntü Düzenleme (TÜM TASARIM BURADA) ---
# Anime gökyüzü arka planı ve yuvarlak input tasarımı
st.markdown("""
    <style>
    /* Tam sayfa anime gökyüzü arka planı */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1518176219326-1e64903ed7bf?q=80&w=1920&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Ana içerik paneli (şeffaf beyaz) */
    .block-container {
        background-color: rgba(255, 255, 255, 0.7);
        padding: 2rem;
        border_radius: 20px;
        backdrop-filter: blur(5px);
        margin-top: 50px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }

    /* Başlık ve metin renkleri */
    h1, p {
        color: #2e6091 !important;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }

    /* TAHMİN ALANI DÜZENİ */
    .predict-row {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    /* Yuvarlak ve küçük input kutusu */
    .stNumberInput input {
        border-radius: 50px;
        border: 2px solid #5d9cec;
        padding: 10px;
        text-align: center;
        font-size: 1.2rem;
        width: 100px;
        font-weight: bold;
    }
    
    /* Input'un başlığını gizle */
    .stNumberInput label {
        display: none;
    }

    /* Artı/Eksi ve Gülen Butonlar */
    .stButton>button {
        border-radius: 50px;
        font-weight: bold;
        transition: all 0.2s;
    }

    /* Artı ve Eksi butonları özel stili */
    .stButton>button[kind="secondary"] {
        background-color: #5d9cec;
        color: white;
        font-size: 1.3rem;
        width: 45px;
        height: 45px;
        border: none;
    }
    .stButton>button[kind="secondary"]:hover {
        background-color: #4a89dc;
        transform: scale(1.1);
    }

    /* Gülen Emoji (Tahmin) Butonu özel stili */
    .stButton>button[kind="primary"] {
        background-color: #ffce54;
        color: #333;
        font-size: 1.5rem;
        width: 60px;
        height: 60px;
        border: none;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .stButton>button[kind="primary"]:hover {
        background-color: #f6bb42;
        transform: scale(1.1) rotate(10deg);
    }
    
    /* Sonuç Mesajları (Warning/Success) */
    .stAlert {
        border-radius: 15px;
    }
    
    </style>
""", unsafe_allow_html=True)

# --- Oyun Mantığı ve Durum Yönetimi ---
if 'hedef_sayi' not in st.session_state:
    st.session_state.hedef_sayi = random.randint(1, 100)
    st.session_state.tahmin_sayisi = 0
if 'current_guess' not in st.session_state:
    st.session_state.current_guess = 50 # Oyun başlangıç tahmini

# --- Arayüz Elemanları ---
st.markdown("<h1 style='text-align: center;'>☁️ Sayı Tahmin Dünyası 🍭</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1rem;'>Bir bulutun arkasına 1 ile 100 arası bir sayı sakladım. Bakalım bulabilecek misin?</p>", unsafe_allow_html=True)


# --- ÖZEL TAHMİN ALANI (Satır Düzeni) ---
# Üç kolon oluştur: [Artı/Eksi] , [Sayı Girişi] , [Gülen Buton]
cols = st.columns([1, 1.5, 1], gap="small")

with cols[0]:
    st.markdown('<div style="display:flex; flex-direction:column; gap:5px; align-items:flex-end; margin-top: 15px;">', unsafe_allow_html=True)
    btn_artir = st.button("+", key="btn_plus", type="secondary")
    btn_azalt = st.button("-", key="btn_minus", type="secondary")
    st.markdown('</div>', unsafe_allow_html=True)

    # Butonlara tıklanınca sayıyı değiştirme mantığı
    if btn_artir and st.session_state.current_guess < 100:
        st.session_state.current_guess += 1
    if btn_azalt and st.session_state.current_guess > 1:
        st.session_state.current_guess -= 1

with cols[1]:
    # Küçük, yuvarlak sayı giriş alanı
    tahmin = st.number_input(
        "Tahmin:",
        min_value=1,
        max_value=100,
        value=st.session_state.current_guess,
        step=1,
        key="main_input"
    )
    # Input alanından elle sayı girilirse session_state'i güncelle
    st.session_state.current_guess = tahmin

with cols[2]:
    st.markdown('<div style="margin-top: 15px;">', unsafe_allow_html=True)
    btn_tahmin = st.button("😊", key="btn_check", type="primary") # Gülen emoji butonu
    st.markdown('</div>', unsafe_allow_html=True)


# --- Tahmin Sonuçları ve Oyun Mantığı ---
st.markdown("<hr style='border: 1px dashed #5d9cec;'>", unsafe_allow_html=True)

# Sonuçların gösterileceği alan
result_container = st.container()

with result_container:
    if btn_tahmin:
        st.session_state.tahmin_sayisi += 1
        
        # Kullanıcının son tahminini inputtan al (artı/eksi butonlarıyla değişmiş olabilir)
        current_tahmin = st.session_state.current_guess
        
        if current_tahmin < st.session_state.hedef_sayi:
            st.warning(f"Cıkk! Daha BÜYÜK bir sayı söylemelisin! ⬆️ (Deneme: {st.session_state.tahmin_sayisi})")
        elif current_tahmin > st.session_state.hedef_sayi:
            st.warning(f"Hımm! Daha KÜÇÜK bir sayı söylemelisin! ⬇️ (Deneme: {st.session_state.tahmin_sayisi})")
        else:
            st.success(f"🎊 HARİKA! {st.session_state.tahmin_sayisi}. denemede doğru bildin! Sayı {st.session_state.hedef_sayi} idi. ⭐")
            st.balloons()
            
            # Yeniden başlat butonu
            if st.button("Tekrar Oyna? 🌀"):
                st.session_state.hedef_sayi = random.randint(1, 100)
                st.session_state.tahmin_sayisi = 0
                st.session_state.current_guess = 50
                st.rerun()
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="DEL-CUT Takım Tasarımcısı", layout="wide")

st.title("DEL-CUT - Parmak Freze Teknik Resim Oluşturucu")
st.markdown("Soldaki menüden **Helis Açısı** ve **Ağız Sayısı** dahil tüm detayları değiştirebilirsiniz.")

# --- KENAR ÇUBUĞU (INPUTLAR) ---
st.sidebar.header("📏 Temel Ölçüler (mm)")
d1 = st.sidebar.number_input("d1 (Kesme Çapı)", value=10.0, step=0.1)
d2 = st.sidebar.number_input("d2 (Şaft Çapı)", value=10.0, step=0.1)
d3 = st.sidebar.number_input("d3 (Boyun Çapı)", value=9.5, step=0.1, help="Kesici arkasındaki boşaltma çapı")
l1 = st.sidebar.number_input("l1 (Tam Boy)", value=75.0, step=1.0)
l2 = st.sidebar.number_input("l2 (Kesme Boyu)", value=25.0, step=1.0)
l3 = st.sidebar.number_input("l3 (Erişim Boyu)", value=30.0, step=1.0)
r  = st.sidebar.number_input("R (Köşe Radyüsü)", value=0.5, step=0.1)

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Geometri Detayları")
flutes = st.sidebar.slider("Z (Ağız Sayısı)", min_value=1, max_value=6, value=4, step=1)
helix_angle = st.sidebar.slider("α (Helis Açısı)", min_value=0, max_value=60, value=30, step=5, help="Standart: 30° veya 45°")

# --- ÇİZİM FONKSİYONU ---
def teknik_resim_ciz(d1, d2, d3, l1, l2, l3, r, flutes, helix_angle):
    # Grafik boyutunu ayarla
    fig, ax = plt.subplots(figsize=(12, 6))
    
    line_color = 'black'
    fill_color = '#e6e6e6' # Metalik gri hissi
    lw = 1.5

    # 1. Şaft (Gövde)
    shaft_rect = patches.Rectangle((l3, -d2/2), l1-l3, d2, linewidth=lw, edgecolor=line_color, facecolor=fill_color)
    ax.add_patch(shaft_rect)

    # 2. Boyun (Ara kısım)
    neck_rect = patches.Rectangle((l2, -d3/2), l3-l2, d3, linewidth=lw, edgecolor=line_color, facecolor=fill_color)
    ax.add_patch(neck_rect)

    # 3. Kesme Kısmı (Ana gövde arka planı)
    # Helisleri üzerine çizeceğimiz için önce boş bir dikdörtgen çiziyoruz
    cutting_rect = patches.Rectangle((r, -d1/2), l2-r, d1, linewidth=lw, edgecolor=line_color, facecolor=fill_color)
    ax.add_patch(cutting_rect)

    # 4. Radyüsler (Köşe yuvarlatmaları)
    arc_top = patches.Arc((r, d1/2 - r), 2*r, 2*r, theta1=90, theta2=180, linewidth=lw, color=line_color)
    ax.add_patch(arc_top)
    arc_bot = patches.Arc((r, -d1/2 + r), 2*r, 2*r, theta1=180, theta2=270, linewidth=lw, color=line_color)
    ax.add_patch(arc_bot)
    
    # Radyüs birleşim çizgileri (Alın ve Yanlar)
    plt.plot([0, 0], [-(d1/2 - r), (d1/2 - r)], color=line_color, linewidth=lw) # Ön yüz
    plt.plot([r, l2], [d1/2, d1/2], color=line_color, linewidth=lw)   # Üst çizgi
    plt.plot([r, l2], [-d1/2, -d1/2], color=line_color, linewidth=lw) # Alt çizgi

    # --- GELİŞMİŞ HELİS ÇİZİMİ (SİNÜS DALGASI) ---
    # Helisler silindir üzerinde dönerken yandan bakıldığında sinüs dalgası gibi görünür.
    
    # X ekseni boyunca noktalar (Radyüs bitiminden kesme boyu sonuna kadar)
    x_points = np.linspace(r, l2, 200)
    
    # Helis Hatvesi (Pitch) Hesabı: P = (pi * D) / tan(helis_açısı)
    # Açıyı radyana çevir
    angle_rad = np.deg2rad(helix_angle)
    if helix_angle > 0:
        pitch = (np.pi * d1) / np.tan(angle_rad)
    else:
        pitch = 999999 # 0 derece ise düz çizgi

    # Her bir ağız için döngü
    for i in range(flutes):
        # Her ağız arasında faz farkı vardır (360 derece / ağız sayısı)
        phase_shift = (2 * np.pi * i) / flutes
        
        # Sinüs dalgası formülü: y = (Çap/2) * sin( (2pi/Pitch)*x + faz )
        y_points = (d1 / 2) * np.sin((2 * np.pi / pitch) * x_points + phase_shift)
        
        # Çizgiyi çiz (hafif gri ve ince)
        ax.plot(x_points, y_points, color='black', alpha=0.4, linewidth=0.8)

    # --- ÖLÇÜLENDİRME ---
    def draw_dim_h(x1, x2, y, text):
        ax.annotate('', xy=(x1, y), xytext=(x2, y), arrowprops=dict(arrowstyle='<->', color='red'))
        ax.text((x1+x2)/2, y+1, text, ha='center', color='red', fontsize=10, fontweight='bold')
        plt.plot([x1, x1], [0, y], 'k--', alpha=0.2, linewidth=0.5)
        plt.plot([x2, x2], [0, y], 'k--', alpha=0.2, linewidth=0.5)

    def draw_dim_v(x, y1, y2, text, offset=0):
        x_pos = x + offset
        ax.annotate('', xy=(x_pos, y1), xytext=(x_pos, y2), arrowprops=dict(arrowstyle='<->', color='blue'))
        ax.text(x_pos+1, (y1+y2)/2, text, va='center', color='blue', fontsize=10, fontweight='bold')
        plt.plot([0, x_pos], [y1, y1], 'k--', alpha=0.2, linewidth=0.5)
        plt.plot([0, x_pos], [y2, y2], 'k--', alpha=0.2, linewidth=0.5)

    max_h = max(d1, d2)
    
    # Yatay Ölçüler
    draw_dim_h(0, l1, -(max_h/2 + 15), f"l1: {l1}")
    draw_dim_h(0, l3, -(max_h/2 + 9), f"l3: {l3}")
    draw_dim_h(0, l2, -(max_h/2 + 3), f"l2: {l2}")
    
    # Dikey Ölçüler
    draw_dim_v(l1, -d2/2, d2/2, f"d2: {d2}", offset=5)
    draw_dim_v(l2, -d3/2, d3/2, f"d3: {d3}", offset=2)
    draw_dim_v(l2/2, -d1/2, d1/2, f"d1: {d1}")

    # Radyüs Oku
    ax.annotate(f"R: {r}", xy=(r*0.4, -d1/2+r*0.2), xytext=(r+5, -d1/2-8),
                arrowprops=dict(facecolor='black', arrowstyle='->'), fontsize=9)

    # Grafik Ayarları
    ax.set_aspect('equal')
    ax.set_xlim(-5, l1 + 25)
    ax.set_ylim(-(max_h + 20), (max_h + 20))
    plt.axis('off')
    return fig

# --- ANA EKRAN GÖRÜNÜMÜ ---
st.subheader("Teknik Resim Önizlemesi")

if l1 > l3 and l3 >= l2:
    fig = teknik_resim_ciz(d1, d2, d3, l1, l2, l3, r, flutes, helix_angle)
    st.pyplot(fig)
else:
    st.error("⚠️ HATA: Boy ölçüleri mantıksız! (l1 > l3 > l2 olmalı)")

# --- BİLGİ KUTUSU ---
col1, col2 = st.columns(2)
with col1:
    st.info(f"**Takım Özellikleri:**\n\n"
            f"- **Ağız Sayısı (Z):** {flutes}\n"
            f"- **Helis Açısı:** {helix_angle}°\n"
            f"- **Çap:** Ø{d1} mm")
with col2:
    st.success(f"**Stok Kodu Önerisi:**\n\n"
               f"EM-{int(d1)}R{r}-{flutes}Z-{int(l2)}")

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="DEL-CUT Takım Tasarımcısı", layout="wide")

st.title("DEL-CUT - Parmak Freze Teknik Resim Oluşturucu")
st.markdown("Soldaki menüden takım parametrelerini girerek teknik resmi güncelleyebilirsiniz.")

# --- KENAR ÇUBUĞU (INPUTLAR) ---
st.sidebar.header("📏 Takım Parametreleri (mm)")

d1 = st.sidebar.number_input("d1 (Kesme Çapı)", value=10.0, step=0.1)
d2 = st.sidebar.number_input("d2 (Şaft Çapı)", value=10.0, step=0.1)
d3 = st.sidebar.number_input("d3 (Boyun Çapı)", value=9.5, step=0.1, help="Kesici arkasındaki boşaltma çapı")
l1 = st.sidebar.number_input("l1 (Tam Boy)", value=75.0, step=1.0)
l2 = st.sidebar.number_input("l2 (Kesme Boyu)", value=25.0, step=1.0)
l3 = st.sidebar.number_input("l3 (Erişim Boyu)", value=30.0, step=1.0)
r  = st.sidebar.number_input("R (Köşe Radyüsü)", value=0.5, step=0.1)

# --- ÇİZİM FONKSİYONU ---
def teknik_resim_ciz(d1, d2, d3, l1, l2, l3, r):
    # Grafik boyutunu ayarla
    fig, ax = plt.subplots(figsize=(10, 5))
    
    line_color = 'black'
    fill_color = '#e6e6e6'
    lw = 1.5

    # 1. Şaft
    shaft_rect = patches.Rectangle((l3, -d2/2), l1-l3, d2, linewidth=lw, edgecolor=line_color, facecolor=fill_color)
    ax.add_patch(shaft_rect)

    # 2. Boyun
    neck_rect = patches.Rectangle((l2, -d3/2), l3-l2, d3, linewidth=lw, edgecolor=line_color, facecolor=fill_color)
    ax.add_patch(neck_rect)

    # 3. Kesme Kısmı
    cutting_rect = patches.Rectangle((r, -d1/2), l2-r, d1, linewidth=lw, edgecolor=line_color, facecolor=fill_color)
    ax.add_patch(cutting_rect)

    # 4. Radyüsler
    arc_top = patches.Arc((r, d1/2 - r), 2*r, 2*r, theta1=90, theta2=180, linewidth=lw, color=line_color)
    ax.add_patch(arc_top)
    arc_bot = patches.Arc((r, -d1/2 + r), 2*r, 2*r, theta1=180, theta2=270, linewidth=lw, color=line_color)
    ax.add_patch(arc_bot)
    
    # Çizgiler
    plt.plot([0, 0], [-(d1/2 - r), (d1/2 - r)], color=line_color, linewidth=lw)
    plt.plot([r, l2], [d1/2, d1/2], color=line_color, linewidth=lw)
    plt.plot([r, l2], [-d1/2, -d1/2], color=line_color, linewidth=lw)

    # Helis Görünümü
    for i in range(0, int(l2), 3):
        plt.plot([i, i+2], [-d1/2, d1/2], color='gray', alpha=0.3, linewidth=1)

    # Ölçü Okları Fonksiyonları
    def draw_dim_h(x1, x2, y, text):
        ax.annotate('', xy=(x1, y), xytext=(x2, y), arrowprops=dict(arrowstyle='<->', color='red'))
        ax.text((x1+x2)/2, y+1, text, ha='center', color='red', fontsize=9)
        # Kesik çizgiler
        plt.plot([x1, x1], [0, y], 'k--', alpha=0.2, linewidth=0.5)
        plt.plot([x2, x2], [0, y], 'k--', alpha=0.2, linewidth=0.5)

    def draw_dim_v(x, y1, y2, text):
        ax.annotate('', xy=(x, y1), xytext=(x, y2), arrowprops=dict(arrowstyle='<->', color='blue'))
        ax.text(x+1, (y1+y2)/2, text, va='center', color='blue', fontsize=9)

    max_h = max(d1, d2)
    # Ölçüleri Çiz
    draw_dim_h(0, l1, -(max_h/2 + 12), f"l1: {l1}")
    draw_dim_h(0, l3, -(max_h/2 + 7), f"l3: {l3}")
    draw_dim_h(0, l2, -(max_h/2 + 2), f"l2: {l2}")
    
    draw_dim_v(l1+2, -d2/2, d2/2, f"d2: {d2}")
    draw_dim_v(l2, -d3/2, d3/2, f"d3: {d3}")
    draw_dim_v(l2/2, -d1/2, d1/2, f"d1: {d1}")

    ax.set_aspect('equal')
    ax.set_xlim(-5, l1 + 10)
    ax.set_ylim(-(max_h + 15), (max_h + 15))
    plt.axis('off')
    return fig

# --- ANA EKRAN ÇIKTISI ---
st.subheader("Teknik Resim Önizlemesi")

# Çizimi oluştur ve göster
if l1 > l3 and l3 >= l2: # Mantıksal kontrol
    fig = teknik_resim_ciz(d1, d2, d3, l1, l2, l3, r)
    st.pyplot(fig)
else:
    st.error("HATA: Boylar arasında mantıksızlık var! (l1 > l3 > l2 olmalı)")

# Verileri Tablo Olarak Göster
st.write("---")
st.write("**Özet Tablo:**")
st.table({
    "Parametre": ["Kesme Çapı (d1)", "Şaft Çapı (d2)", "Tam Boy (l1)", "Kesme Boyu (l2)"],
    "Değer (mm)": [d1, d2, l1, l2]
})
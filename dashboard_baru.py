import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# styling biar grafik keliatan cakep
# styling biar grafik vibe putih & clean
# styling dinamis sesuai pilihan tema
sns.set_style("whitegrid")
plt.style.use("default")


st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# ---- Cek kolom cuaca, soalnya tiap dataset bisa beda nama kolom ----
def pick_weather_col(df):
    kandidat = ['cuaca', 'kondisi_cuaca', 'weathersit', 'weather']
    for c in kandidat:
        if c in df.columns:
            return c
    return None  # kalau ga nemu, nanti bakal kasih info di UI

# ---- load data yang udah di export dari notebook ----
day = pd.read_csv("day_data_bike.csv")

# cek file jam, siapa tau namanya beda (biar ga drama error)
import os
hour_file = None
for cek in ["all_data_bike.csv","hour_data_bike.csv","hour_data.csv"]:
    if os.path.exists(cek):
        hour_file = cek
        break

hour = pd.read_csv(hour_file) if hour_file else pd.DataFrame()

# ubah kolom tanggal jadi datetime, wajib!
day['tanggal'] = pd.to_datetime(day['tanggal'], errors='coerce')
if not hour.empty:
    hour['tanggal'] = pd.to_datetime(hour['tanggal'], errors='coerce')

# debug mode biar tau kolom apa aja yang ada (nanti boleh hapus kalau udah fix)
with st.expander("cek kolom data (klik kalau mau lihat)"):
    st.write("kolom data harian:", day.columns.tolist())
    if not hour.empty:
        st.write(f"kolom data jam ({hour_file}):", hour.columns.tolist())

# min & max tanggal buat input filter
min_date = day['tanggal'].min()
max_date = day['tanggal'].max()

# ---- sidebar buat filter tanggal + logo biar rada aesthetic ----
with st.sidebar:
    st.image("https://cdn.lyft.com/static/bikesharefe/logo/CapitalBikeshare-main.svg", width=200)
    # pilih tema
    theme = st.sidebar.radio(
        "Pilih tema tampilan:",
        ("🌞 Light Mode", "🌙 Dark Mode")
)

    start_date, end_date = st.date_input(
        "Pilih tanggal (sesuai mood 🤭)",
        value=(min_date.date(), max_date.date()),
        min_value=min_date.date(),
        max_value=max_date.date()
    )

# convert input jadi Timestamp (kalau ga nanti Streamlit ngambek)
start = pd.to_datetime(start_date)
end = pd.to_datetime(end_date)

# filter data sesuai tanggal yang dipilih
df_day = day[(day['tanggal'] >= start) & (day['tanggal'] <= end)].copy()
df_hour = hour[(hour['tanggal'] >= start) & (hour['tanggal'] <= end)].copy() if not hour.empty else pd.DataFrame()
# aktifkan tema sesuai pilihan user
if theme == "🌞 Light Mode":
    sns.set_style("whitegrid")
    plt.style.use("default")
else:
    sns.set_style("darkgrid")
    plt.style.use("default")


# cari kolom cuaca yang valid
weather_col = pick_weather_col(df_day)

# jaga-jaga kalau nama kolom penyewa beda
if 'total_penyewa' not in df_day.columns:
    if 'cnt' in df_day.columns:
        df_day = df_day.rename(columns={'cnt':'total_penyewa'})
    elif 'count' in df_day.columns:
        df_day = df_day.rename(columns={'count':'total_penyewa'})

# group-group data buat chart
season_df = df_day.groupby(['musim','tahun'], observed=False)['total_penyewa'].sum().reset_index() if 'musim' in df_day.columns else pd.DataFrame()
weather_df = df_day.groupby([weather_col,'tahun'], observed=False)['total_penyewa'].sum().reset_index() if weather_col else pd.DataFrame()
monthly_df = df_day.groupby(['bulan','tahun'], observed=False)[['casual','registered']].sum().reset_index() if 'bulan' in df_day.columns else pd.DataFrame()

pivot_df = df_hour.pivot_table(index='seminggu', columns='jam', values='total_penyewa', aggfunc='mean') \
    if not df_hour.empty and {'seminggu','jam','total_penyewa'}.issubset(df_hour.columns) \
    else pd.DataFrame()

# ==== mulai tampilkan dashboard-nya ====
st.title("🚲 Dashboard Penyewaan Sepeda")

# grafik musim
if not season_df.empty:
    st.subheader("🌤️ Pengaruh musim ke jumlah penyewa")
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(data=season_df, x="musim", y="total_penyewa", hue="tahun", ax=ax)
    st.pyplot(fig)
# insight otomatis - musim
if not season_df.empty:
    musim_group = season_df.groupby("musim")["total_penyewa"].sum()

    if not musim_group.empty:
        musim_top = musim_group.idxmax()
        total_top = musim_group.max()

        st.markdown(f"""
        🍃 **Insight Musim**

        Rentang **{start.date()} – {end.date()}** didominasi oleh musim **{musim_top}**  
        dengan total **{total_top:,}** peminjaman sepeda 🚲
        """)
    

else:
    st.info("Data musim belum tersedia / beda nama kolom (cek export notebook ya 😉)")

# grafik cuaca
if not weather_df.empty:
    st.subheader("☁️ Cuaca vs jumlah penyewa")
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(data=weather_df, x=weather_col, y="total_penyewa", hue="tahun", ax=ax)
    st.pyplot(fig)
# insight otomatis - cuaca
if not weather_df.empty:
    cuaca_group = weather_df.groupby(weather_col)["total_penyewa"].sum()

    if not cuaca_group.empty:
        cuaca_top = cuaca_group.idxmax()
        total_cuaca = cuaca_group.max()

        st.markdown(f"""
        🌤️ **Insight Cuaca**

        Dalam periode **{start.date()} – {end.date()}**, kondisi cuaca paling mendukung penyewaan adalah  
        **{cuaca_top}**, dengan total **{total_cuaca:,}** peminjaman.  
        """)
    

else:
    st.info("Kolom cuaca ga ketemu, skip dulu ya 😅")

# grafik monthly casual vs registered
if not monthly_df.empty:
    st.subheader("📈 Tren penyewa (Casual vs Registered)")
    fig, ax = plt.subplots(figsize=(10,5))
    sns.lineplot(data=monthly_df, x="bulan", y="casual", marker="o", label="Casual")
    sns.lineplot(data=monthly_df, x="bulan", y="registered", marker="o", label="Registered")
    st.pyplot(fig)
  # insight otomatis - casual vs registered
if not monthly_df.empty:
    total_casual = monthly_df["casual"].sum()
    total_reg = monthly_df["registered"].sum()

    winner = "Registered" if total_reg > total_casual else "Casual"

    st.markdown(f"""
    👥 **Insight Tipe Pengguna**
    Dalam periode **{start.date()} – {end.date()}**, pengguna **{winner}** lebih mendominasi 🚴‍♂️

    - Casual: **{total_casual:,}**
    - Registered: **{total_reg:,}**
    """)
  


# heatmap pola jam & hari
if not pivot_df.empty:
    st.subheader("🔥 Pola Penyewaan Berdasarkan jam & hari (Heatmap)")
    fig, ax = plt.subplots(figsize=(12,6))
    sns.heatmap(pivot_df, cmap="YlGnBu", ax=ax)
    st.pyplot(fig)
 # insight otomatis - hari & jam
if not df_hour.empty:
    top_day = df_hour.groupby("seminggu")["total_penyewa"].sum().idxmax()
    top_hour = df_hour.groupby("jam")["total_penyewa"].sum().idxmax()

    st.markdown(f"""
    🕒 **Insight Waktu Ramai**

    - Hari paling ramai: **{top_day}**
    - Jam puncak: **{top_hour}:00**

    Cocok buat ngatur shift maintenance & supply sepeda 💡
    """)

  

else:
    st.info("Data jam belum tersedia / nama kolom beda")
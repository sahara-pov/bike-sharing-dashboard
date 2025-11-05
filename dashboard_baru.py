# =========================================
# Import library
# =========================================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================================
# Load dataset
# =========================================
day_df = pd.read_csv("day_data_bike.csv")
hour_df = pd.read_csv("hour_data_bike.csv")

# pastikan tanggal sudah datetime
day_df['tanggal'] = pd.to_datetime(day_df['tanggal'])
hour_df['tanggal'] = pd.to_datetime(hour_df['tanggal'])

# =========================================
# Sidebar - Filter data
# =========================================
with st.sidebar:
    st.title("⚙️ Pengaturan")
    
    # Mode tampilan
    theme = st.radio("Tema Dashboard:", ["☀️ Light", "🌙 Dark"])
    
    # Rentang tanggal
    min_date = day_df['tanggal'].min().date()
    max_date = day_df['tanggal'].max().date()

    tanggal = st.date_input("Pilih rentang tanggal:",
                            (min_date, max_date),
                            min_value=min_date,
                            max_value=max_date)

# antisipasi jika hanya satu tanggal dipilih
try:
    start_date, end_date = tanggal
except:
    start_date = end_date = tanggal

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# filter dataset sesuai tanggal
filtered_day = day_df[(day_df['tanggal'] >= start_date) & (day_df['tanggal'] <= end_date)]
filtered_hour = hour_df[(hour_df['tanggal'] >= start_date) & (hour_df['tanggal'] <= end_date)]

# =========================================
# Tema Matplotlib
# =========================================
if theme == "☀️ Light":
    sns.set_style("whitegrid")
else:
    sns.set_style("darkgrid")
    plt.style.use("dark_background")

# =========================================
# Judul Dashboard
# =========================================
st.title("🚲 Bike Sharing Dashboard")
st.write("Dashboard ini menampilkan analisis penyewaan sepeda berdasarkan data harian dan per jam.")

# =========================================
# Grafik 1 - Pengaruh Musim
# =========================================
st.subheader("🍂 Penyewaan Berdasarkan Musim")
musim_df = filtered_day.groupby("musim")["total_penyewa"].sum().reset_index()

fig, ax = plt.subplots(figsize=(8,4))
sns.barplot(data=musim_df, x='musim', y='total_penyewa', palette='coolwarm', ax=ax)
ax.set_title("Total Penyewa Sepeda per Musim")
st.pyplot(fig)

# insight
musim_top = musim_df.loc[musim_df['total_penyewa'].idxmax(),'musim']
musim_val = musim_df['total_penyewa'].max()

st.write(f"🍂 Dalam rentang waktu ini, musim paling ramai adalah **{musim_top}** dengan **{musim_val:,}** penyewaan.")


# =========================================
# Grafik Pengaruh Cuaca
# =========================================
st.subheader("🌦️ Penyewaan Berdasarkan Kondisi Cuaca")
cuaca_col = "kondisi_cuaca" if "kondisi_cuaca" in filtered_day.columns else "cuaca"
cuaca_df = filtered_day.groupby(cuaca_col)["total_penyewa"].sum().reset_index()

fig, ax = plt.subplots(figsize=(8,4))
sns.barplot(data=cuaca_df, x=cuaca_col, y='total_penyewa', palette='coolwarm', ax=ax)
ax.set_title("Pengaruh Cuaca terhadap Penyewaan")
st.pyplot(fig)

# insight
cuaca_top = cuaca_df.loc[cuaca_df['total_penyewa'].idxmax(), cuaca_col]
cuaca_val = cuaca_df['total_penyewa'].max()

st.write(f"🌦️ Cuaca paling mendukung penyewaan di periode ini adalah **{cuaca_top}** dengan **{cuaca_val:,}** peminjam.")


# =========================================
# Grafik 2 - Weekday vs Weekend
# =========================================
st.subheader("📅 Perbandingan Weekday & Weekend")
hari_df = filtered_day.groupby("kategori_hari")["total_penyewa"].sum().reset_index()

fig, ax = plt.subplots(figsize=(8,4))
sns.barplot(data=hari_df, x='kategori_hari', y='total_penyewa', palette='viridis', ax=ax)
ax.set_title("Total Penyewa: Weekday vs Weekend")
st.pyplot(fig)

# insight
hari_top = hari_df.loc[hari_df['total_penyewa'].idxmax(),'kategori_hari']
hari_val = hari_df['total_penyewa'].max()

st.write(f"📅 Selama rentang ini, penyewaan paling tinggi terjadi pada **{hari_top}** dengan **{hari_val:,}** penyewa.")

# =========================================
# Grafik 3 - Tren performa bisnis 2 tahun ini
# =========================================
st.subheader("📈 Performa Bisnis (Total Penyewa per Bulan)")
trend = filtered_day.resample('M', on='tanggal')['total_penyewa'].sum()

fig, ax = plt.subplots(figsize=(10,4))
sns.lineplot(x=trend.index, y=trend.values, marker='o', ax=ax)
ax.set_title("Tren Total Penyewa Sepeda per Bulan")
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Penyewa")
st.pyplot(fig)

# Insight
peak_month = trend.idxmax().strftime('%B %Y')
peak_val = trend.max()

st.write(f"🚀 Puncak penyewaan terjadi pada **{peak_month}** dengan **{peak_val:,}** penyewa.")


# =========================================
# Grafik 4 - Casual vs Registered
# =========================================
st.subheader("👥 Casual vs Registered")
monthly = filtered_day.groupby("bulan")[['casual','registered']].sum().reset_index()

fig, ax = plt.subplots(figsize=(10,4))
sns.lineplot(data=monthly, x='bulan', y='casual', marker='o', label='Casual')
sns.lineplot(data=monthly, x='bulan', y='registered', marker='o', label='Registered')
ax.set_title("Tren Casual vs Registered")
st.pyplot(fig)

# Insight
tot_casual = monthly['casual'].sum()
tot_reg = monthly['registered'].sum()
lebih_banyak = "Registered" if tot_reg > tot_casual else "Casual"

st.write(f"👥 Dalam periode ini, pengguna **{lebih_banyak}** lebih banyak menyewa sepeda.")
st.write(f"- Total Casual: **{tot_casual:,}**")
st.write(f"- Total Registered: **{tot_reg:,}**")


# =========================================
# Grafik 5 - Heatmap Jam vs Hari
# =========================================
st.subheader("⏰ Pola Penggunaan Jam & Hari (Heatmap)")

if not filtered_hour.empty:
    pivot = filtered_hour.pivot_table(
        index='seminggu',
        columns='jam',
        values='total_penyewa',
        aggfunc='mean'
    )

    fig, ax = plt.subplots(figsize=(12,5))
    sns.heatmap(pivot, cmap='YlGnBu', ax=ax)
    ax.set_title("Rata-Rata Penyewaan per Jam per Hari")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Hari")
    st.pyplot(fig)

    # insight dinamis (ikut rentang tanggal)
    jam_peak = filtered_hour.groupby('jam')['total_penyewa'].mean().idxmax()
    hari_peak = filtered_hour.groupby('seminggu')['total_penyewa'].mean().idxmax()

    st.write(
        f"🔥 Dalam rentang waktu ini, waktu paling rame adalah **{hari_peak} jam {jam_peak}:00**."
    )
else:
    st.write("⚠️ Tidak ada data pada rentang tanggal ini.")

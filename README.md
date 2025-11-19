# bike-sharing-dashboard
Dashboard Analisis Bisnis Rental Sepeda CAPITAL BIKESHARE
# 🚲 Bike Sharing Analysis & Dashboard – Capital Bikeshare
![Capital Bikeshare](https://cdn.lyft.com/static/bikesharefe/logo/CapitalBikeshare-main.svg)


Proyek ini menganalisis data penyewaan sepeda dari sistem **Capital Bikeshare** (Washington D.C) dan membangun dashboard interaktif menggunakan **Streamlit** untuk melihat pola penggunaan sepeda berdasarkan waktu, musim, cuaca, dan tipe pengguna.

Dataset:  
[Kaggle – Bike Sharing Dataset](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset)

---

## 🎯 Tujuan Proyek

- Memahami pola penyewaan sepeda berdasarkan waktu & musim
- Menganalisis dampak cuaca pada penggunaan sepeda
- Membandingkan pengguna **casual** vs **registered**
- Membangun dashboard interaktif untuk eksplorasi data fleksibel
- Memberikan insight data secara otomatis sesuai rentang tanggal yang dipilih

---

## 📦 Teknologi yang Digunakan

| Tools / Library | Keterangan |
|---|---|
Python | Bahasa pemrograman utama
Pandas | Pembersihan & manipulasi data
Matplotlib & Seaborn | Visualisasi data
Streamlit | Dashboard interaktif
Jupyter Notebook | Eksplorasi & EDA

---

## 📊 Fitur Dashboard

- Filter tanggal dinamis
- Tema **Light Mode / Dark Mode toggle**
- Visualisasi:
  - Jumlah penyewa berdasarkan musim
  - Pengaruh kondisi cuaca
  - Tren bulanan (Casual vs Registered)
  - Heatmap pola jam & hari
- Insight otomatis di bawah grafik ✨

---

## 🔍 Insight Utama

- **Musim panas & gugur** memiliki jumlah penyewaan tertinggi  
- **Cuaca cerah** → penggunaan sepeda meningkat signifikan  
- Pengguna **registered** mendominasi, artinya banyak pengguna rutin/komuter
- Jam ramai: siang hingga sore, terutama weekday

---
## 📂 Struktur Folder Submission
submission
├───dashboard
| ├───main_data.csv
| └───dashboard.py
├───data
| ├───data_1.csv
| └───data_2.csv
├───notebook.ipynb
├───README.md
└───requirements.txt
└───url.txt

---
## 📁 Struktur Project
bike_sharing_dashboard/ <br>
├── dashboard_baru.py # file utama Streamlit<br>
├── day_data_bike.csv # data harian setelah clean<br>
├── all_data_bike.csv # data jam + clean data<br>
├── requirements.txt # library yang diperlukan<br>
└── README.md # file ini<br>

---

## ▶️ Cara Menjalankan

### 1. Clone repositori <br>
```bash
git clone https://github.com/sahara-pov/bike-sharing-dashboard.git
cd bike-sharing-dashboard
```
### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Jalankan dashboard
```
streamlit run dashboard_baru.py
```

Streamlit akan terbuka di browser ✨

## 🌐 Deploy (Streamlit Cloud)

Repository ini dapat dideploy langsung di Streamlit Cloud:

https://bike-sharing-dashboard-by-anisasahara-ds01.streamlit.app/


Input file utama: dashboard_baru.py

---

## 📚 Sumber Data

Kaggle Bike Sharing Dataset

Data tahun 2011–2012

Sudah melalui proses:

- Cleaning

- Feature engineering

- Penamaan kolom ke Bahasa Indonesia

## 👤 About Me

Hi! 👋
Proyek ini dibuat sebagai bagian dari pembelajaran data analysis.

Fokus skill yang dipelajari:

- Data Cleaning & EDA

- Visualisasi data

- Streamlit dashboard

- Insight generation

Feel free to connect or ask questions 🤝

⭐ Kalau suka project ini, jangan lupa kasih star ya! ⭐







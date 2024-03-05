import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
import numpy as np

st.set_page_config(page_title="Air Quality Analysis Dashboard")

st.title("Air Quality Analysis Dashboard")

data = pd.read_csv("dashboard/main_data.csv")

data["datetime"] = pd.to_datetime(data["datetime"])

selected_month = st.sidebar.selectbox("Pilih Bulan", list(data["datetime"].dt.month_name().unique()))
selected_year = st.sidebar.selectbox("Pilih Tahun", list(data["datetime"].dt.year.unique()))
selected_station = st.sidebar.selectbox("Pilih Stasiun", list(data["station"].unique()))

data_filtered = data[(data["datetime"].dt.month_name() == selected_month) & (data["datetime"].dt.year == selected_year) & (data["station"] == selected_station)].copy()

st.subheader("Data pada bulan, tahun, dan stasiun yang diinginkan")
st.write(data_filtered.head())

st.subheader("Kadar PM2.5 Harian")
selected_pollutant = st.selectbox("Pilih Kadar Polusi", ["PM2.5", "PM10", "SO2", "NO2", "CO"])
fig, ax = plt.subplots()
ax.plot(data_filtered["datetime"].dt.day, data_filtered[selected_pollutant])
plt.xlabel("Tanggal")
plt.ylabel("Kadar PM2.5")
st.pyplot(fig)

st.subheader("Korelasi antar Indikator Kualitas Udara")
selected_indicator = st.multiselect("Pilih Indikator untuk Korelasi", data.select_dtypes("float64").columns, default = ["PM2.5", "PM10", "SO2", "NO2", "CO"])
corr = data_filtered.select_dtypes("float64")[selected_indicator].corr()
fig, ax = plt.subplots()
sns.heatmap(corr, cmap = "coolwarm", ax=ax)
plt.title("Korelasi antar Indikator Kualitas Udara")
st.pyplot(fig)

st.subheader("Analisis Arah Angin")
selected_pollutant2 = st.selectbox("Pilih Kadar Polusii", ["PM2.5", "PM10", "SO2", "NO2", "CO"])
data_wind = data_filtered.groupby("wd")[selected_pollutant2].mean()
fig = plt.figure(figsize = (8, 6))
ax = fig.add_subplot(111, polar = True)
theta = np.linspace(0, 2 * np.pi, len(data_wind))
bars = ax.bar(theta, data_wind.values, align = "center", alpha = 0.5)
plt.title("Kadar " + selected_pollutant2 + " dengan arah angin")
st.pyplot(fig)

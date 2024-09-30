import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
data_files = [
    "data/PRSA_Data_Aotizhongxin_20130301-20170228.csv",
    "data/PRSA_Data_Changping_20130301-20170228.csv",
    "data/PRSA_Data_Dingling_20130301-20170228.csv",
    "data/PRSA_Data_Dongsi_20130301-20170228.csv",
    "data/PRSA_Data_Guanyuan_20130301-20170228.csv",
    "data/PRSA_Data_Gucheng_20130301-20170228.csv",
    "data/PRSA_Data_Huairou_20130301-20170228.csv",
    "data/PRSA_Data_Nongzhanguan_20130301-20170228.csv",
    "data/PRSA_Data_Shunyi_20130301-20170228.csv",
    "data/PRSA_Data_Tiantan_20130301-20170228.csv",
    "data/PRSA_Data_Wanliu_20130301-20170228.csv",
    "data/PRSA_Data_Wanshouxigong_20130301-20170228.csv"
]

dfs = []
for file in data_files:
    df = pd.read_csv(file)
    station_name = file.split("_")[2]
    df['station'] = station_name
    dfs.append(df)

# Combine all DataFrames into one
combined_df = pd.concat(dfs)

# Check if the required columns exist
required_columns = ['month', 'year', 'CO']
for col in required_columns:
    if col not in combined_df.columns:
        st.error(f"Error: Column '{col}' not found in the data.")
        st.stop()

# Create dashboard
st.title("Analisis Data Kualitas Udara di Beijing")

# Select station
stations = combined_df['station'].unique()
stasiun = st.selectbox("Pilih Stasiun", stations)

# Display station data
st.write(f"Data Stasiun {stasiun}")
st.write(combined_df[combined_df['station'] == stasiun].head())

# Display monthly CO trend
st.write("Tren Kadar CO Bulanan")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=combined_df[combined_df['station'] == stasiun], x="month", y="CO", marker="o")
plt.title(f"Tren Kadar CO Bulanan di Stasiun {stasiun}")
st.pyplot(fig)

# Display yearly CO trend
st.write("Tren Kadar CO Tahunan")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=combined_df[combined_df['station'] == stasiun], x="year", y="CO", marker="o")
plt.title(f"Tren Kadar CO Tahunan di Stasiun {stasiun}")
st.pyplot(fig)

# Display comparison of monthly CO trends across all stations
st.write("Perbandingan Tren Kadar CO Bulanan di Semua Stasiun")
combined_df_month = combined_df.groupby(["month", "station"])["CO"].mean().reset_index()
fig, ax = plt.subplots(figsize=(12, 8))
sns.lineplot(data=combined_df_month, x="month", y="CO", hue="station", marker="o")
plt.title("Perbandingan Tren Kadar CO Bulanan di Semua Stasiun")
st.pyplot(fig)

# Display comparison of yearly CO trends across all stations
st.write("Perbandingan Tren Kadar CO Tahunan di Semua Stasiun")
combined_df_year = combined_df.groupby(["year", "station"])["CO"].mean().reset_index()
fig, ax = plt.subplots(figsize=(12, 8))
sns.lineplot(data=combined_df_year, x="year", y="CO", hue="station", marker="o")
plt.title("Perbandingan Tren Kadar CO Tahunan di Semua Stasiun")
st.pyplot(fig)
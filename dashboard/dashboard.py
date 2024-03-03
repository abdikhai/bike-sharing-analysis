import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load data
all_df = pd.read_csv("main_data.csv")

# Set theme
sns.set_theme(style="darkgrid")

# Helper functions
def create_most_used_season_df(df):
    most_used_season = df.groupby('season_x')['cnt_x'].sum().reset_index()
    sea = {1: 'musim semi', 2: 'musim panas', 3: 'musim gugur', 4: 'musim dingin'}
    most_used_season['season_x'].replace(sea, inplace=True)
    most_used_season.rename(columns={'season_x': 'musim', 'cnt_x': 'total_peminjaman'}, inplace=True)
    most_used_season = most_used_season.sort_values(by='total_peminjaman', ascending=False)
    return most_used_season

def create_hourly_rentals_df(df):
    hourly_rentals_df = df.groupby('hr')['cnt_y'].sum().reset_index().sort_values(by='cnt_y', ascending=False).reset_index(drop=True)
    return hourly_rentals_df

def create_weekday_rentals_df(df):
    weekday_mapping = {0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}
    weekday_analysis_result_sorted = df.groupby('weekday_y')['cnt_y'].sum().reset_index().sort_values(by='cnt_y', ascending=False).reset_index(drop=True)
    weekday_analysis_result_sorted['weekday_y'] = weekday_analysis_result_sorted['weekday_y'].map(weekday_mapping)
    return weekday_analysis_result_sorted

def create_hour_analysis_df(df):
    hour_analysis_result_sorted = df.groupby(['weekday_y', 'hr'])['cnt_y'].sum().reset_index()
    hour_analysis_result_sorted = hour_analysis_result_sorted.sort_values(by='cnt_y', ascending=False).reset_index(drop=True)
    # Membuat kamus untuk mengganti nilai 'weekday_y' dengan nama hari yang sesuai
    weekday_mapping = {0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}
    hour_analysis_result_sorted['weekday_y'] = hour_analysis_result_sorted['weekday_y'].map(weekday_mapping)
    return hour_analysis_result_sorted


def create_rentals_comparison_df(df):
    rentals_comparison = df.groupby('workingday_y')['cnt_y'].sum().reset_index()
    rentals_comparison['workingday_y'] = rentals_comparison['workingday_y'].replace({0: 'Hari Libur', 1: 'Hari Kerja'})
    return rentals_comparison


with st.sidebar:

    # Menambahkan logo perusahaan
    st.image("https://upload.wikimedia.org/wikipedia/commons/7/77/Streamlit-logo-primary-colormark-darktext.png")
    st.write('Hak Cipta (C) © 2024 oleh Khairul Abdi ')
    # link dataset
    url = "https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset"
    link_text = "Kunjungi Dataset Kaggle"
    st.write('Dataset Bike Sharing')
    st.write(f"[{link_text}]({url})")

#Menyiapkan berbagai dataframe
most_used_season_df = create_most_used_season_df(all_df)
hourly_rentals_df = create_hourly_rentals_df(all_df)
weekday_rentals_df = create_weekday_rentals_df(all_df)
hour_analysis_df = create_hour_analysis_df(all_df)
rentals_comparison_df = create_rentals_comparison_df(all_df)

# Most Used Season
st.header('Dashboard Peminjaman Sepeda :bike:')
st.subheader("Musim yang Digunakan untuk Bersepeda")
col1, col2 = st.columns(2)
with col1:
    max_rentals_season = most_used_season_df.iloc[0]
    st.markdown(f"Musim yang Paling Banyak Digunakan untuk Bersepeda: **{max_rentals_season['musim']}**")
with col2:
    st.markdown(f"Total Peminjaman dalam Musim Ini: **{int(max_rentals_season['total_peminjaman']):,}**")

# Plot for Most Used Season
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='musim', y='total_peminjaman', data=most_used_season_df, ax=ax)
ax.set_xlabel('Musim')
ax.set_ylabel('Total Peminjaman')
ax.set_title('Musim yang Paling Banyak Digunakan untuk Bersepeda')
st.pyplot(fig)
plt.close()

# Hourly Rentals
st.subheader("Distribusi Peminjaman per Jam")
most_rented_hour = hourly_rentals_df.iloc[0]['hr']
total_rentals_most_hour = hourly_rentals_df.iloc[0]['cnt_y']
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"Jam Paling Banyak Dipinjam: **{most_rented_hour}**")
with col2:
    st.markdown(f"Total Peminjaman pada Jam Ini: **{total_rentals_most_hour:,}**")

# Plot for Hourly Rentals
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='hr', y='cnt_y', data=hourly_rentals_df, ax=ax)
ax.set_xlabel('Jam dalam Sehari')
ax.set_ylabel('Total Peminjaman')
ax.set_title('Distribusi Peminjaman per Jam')

hourly_rentals_df_sorted = hourly_rentals_df.sort_values(by='hr', ascending=True) #
ax.plot(hourly_rentals_df_sorted['hr'], hourly_rentals_df_sorted['cnt_y'], color='red', marker='o')
st.pyplot(fig)
plt.close()

# Weekday Rentals
st.subheader("Distribusi Peminjaman per Hari")
most_rented_weekday = weekday_rentals_df.iloc[0]['weekday_y']
total_rentals_most_weekday = weekday_rentals_df.iloc[0]['cnt_y']
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"Hari Paling Banyak Dipinjam: **{most_rented_weekday}**")
with col2:
    st.markdown(f"Total Peminjaman pada Hari Ini: **{total_rentals_most_weekday:,}**")

# Plot for Weekday Rentals Distribution
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='weekday_y', y='cnt_y', data=weekday_rentals_df, ax=ax)
ax.set_xlabel('Hari dalam Seminggu')
ax.set_ylabel('Total Peminjaman')
ax.set_title('Distribusi Peminjaman per Hari')
st.pyplot(fig)
plt.close()

# Hour and Week Rentals
st.subheader("Distribusi Peminjaman per Jam dan Hari")
most_rented_hour_weekday = hour_analysis_df.iloc[0][['hr', 'weekday_y']]
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"Jam Paling Banyak Dipinjam Selama Minggu: **{most_rented_hour_weekday['hr']}**")
with col2:
    st.markdown(f"Pada: **{most_rented_hour_weekday['weekday_y']}**")

# Menampilkan plot Hour and Week Rentals
top_10_most_used_hour_per_day = hour_analysis_df.head(10)
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(top_10_most_used_hour_per_day['hr'].astype(str) + '-' + top_10_most_used_hour_per_day['weekday_y'], top_10_most_used_hour_per_day['cnt_y'], color='skyblue')
ax.set_xlabel('Jam dan Hari')
ax.set_ylabel('Jumlah Penggunaan')
ax.set_title('Distribusi jam penggunaan sepeda per hari dalam seminggu')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig)
plt.close()

# Rentals Comparison between Weekdays and Weekends
st.subheader("Perbandingan Peminjaman antara Hari Kerja dan Hari Libur")
most_rented_day_type = rentals_comparison_df.iloc[1]['workingday_y']
total_rentals_most_day_type = rentals_comparison_df.iloc[1]['cnt_y']
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"Jenis Hari dengan Peminjaman Paling Banyak: **{most_rented_day_type}**")
with col2:
    st.markdown(f"Total Peminjaman pada Jenis Hari Ini: **{total_rentals_most_day_type}**")


# Plot for Rentals Comparison between Weekdays and Weekends
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x='workingday_y', y='cnt_y', data=rentals_comparison_df, ax=ax)
ax.set_xlabel('Jenis Hari')
ax.set_ylabel('Total Peminjaman')
ax.set_title('Perbandingan Peminjaman antara Hari Kerja dan Hari Libur')
st.pyplot(fig)
plt.close()

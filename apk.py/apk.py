import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dan siapkan data
df = pd.read_csv('day.csv')
df['dteday'] = pd.to_datetime(df['dteday'])

season_dict = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
weekday_dict = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',
                4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
weathersit_dict = {1: 'Clear', 2: 'Mist + Cloudy', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow'}

df['season'] = df['season'].map(season_dict)
df['weekday'] = df['weekday'].map(weekday_dict)
df['weathersit'] = df['weathersit'].map(weathersit_dict)
df['day_type'] = df['workingday'].apply(lambda x: 'Weekday' if x == 1 else 'Weekend')

# Judul Aplikasi
st.title('🚲 Bike Sharing Analysis Dashboard')

# Sidebar Filter
st.sidebar.header('Filter Data')
season_filter = st.sidebar.multiselect("Pilih Musim", df['season'].unique(), default=df['season'].unique())
year_filter = st.sidebar.multiselect("Pilih Tahun", df['yr'].unique(), default=df['yr'].unique())

# Filter DataFrame
df_filtered = df[(df['season'].isin(season_filter)) & (df['yr'].isin(year_filter))]

# Visualisasi 1: Tren Penyewaan
st.subheader('📈 Tren Penyewaan Harian')
fig1, ax1 = plt.subplots()
sns.lineplot(data=df_filtered, x='dteday', y='cnt', ax=ax1)
ax1.set_xlabel('Tanggal')
ax1.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig1)

# Visualisasi 2: Perbandingan Casual vs Registered
st.subheader('👥 Perbandingan Casual dan Registered')
casual_sum = df_filtered.groupby('day_type')['casual'].mean()
registered_sum = df_filtered.groupby('day_type')['registered'].mean()

fig2, ax2 = plt.subplots()
bar_width = 0.4
x = casual_sum.index
ax2.bar(x, casual_sum, width=bar_width, label='Casual', color='skyblue')
ax2.bar(x, registered_sum, width=bar_width, label='Registered', bottom=casual_sum, color='salmon')
ax2.set_ylabel('Rata-rata Jumlah Penyewa')
ax2.legend()
st.pyplot(fig2)

# Statistik Ringkasan
st.subheader("📊 Statistik Ringkasan")
st.write(df_filtered[['casual', 'registered', 'cnt']].describe())

# Footer
st.markdown("---")
st.markdown("🧑‍💻 Dibuat untuk Proyek Analisis Data Dicoding")

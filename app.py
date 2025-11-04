import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ⬇️ this must be the first Streamlit command
st.set_page_config(
    page_title="YouTube Video Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Optional: force light background (for Safari issue)
st.markdown(
    "<style>body {background-color: white !important; color: black !important;}</style>",
    unsafe_allow_html=True
)

st.title("📊 YouTube Video Analysis Dashboard")


uploaded_file = st.file_uploader("Upload YouTube Trending Data CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Data loaded successfully!")
else:
    st.warning("⚠️ No file uploaded. Using sample data.")
    data = {
        'video_id': ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9', 'J10'],
        'title': ['Music Hit 1', 'Funny Clip', 'Breaking News', 'Vlog', 'Music Hit 2', 'Game Review', 'News Update', 'Interview', 'Music Hit 3', 'Sketch'],
        'category': ['Music', 'Entertainment', 'News', 'Vlogs', 'Music', 'Gaming', 'News', 'Entertainment', 'Music', 'Entertainment'],
        'views': [1500000, 800000, 1200000, 300000, 2000000, 500000, 900000, 700000, 1800000, 600000],
        'likes': [150000, 50000, 80000, 10000, 200000, 25000, 60000, 40000, 190000, 35000],
        'comment_count': [5000, 1500, 2500, 300, 7000, 800, 1800, 1200, 6500, 1000],
        'publish_time': ['2023-10-25T18:00:00Z', '2023-10-26T14:30:00Z', '2023-10-27T09:00:00Z', '2023-10-27T16:00:00Z', '2023-10-28T18:30:00Z', '2023-10-28T10:00:00Z', '2023-10-29T11:00:00Z', '2023-10-29T20:00:00Z', '2023-10-29T19:00:00Z', '2023-10-30T15:00:00Z']
    }
    df = pd.DataFrame(data)

# --- 2. Data Cleaning ---
df.drop_duplicates(subset=['video_id'], inplace=True)
df.dropna(inplace=True)
top_categories = ['Music', 'Entertainment', 'News']
df['standard_category'] = df['category'].apply(lambda x: x if x in top_categories else 'Others')
df['publish_time'] = pd.to_datetime(df['publish_time'])
df['publish_hour'] = df['publish_time'].dt.hour
df['publish_day'] = df['publish_time'].dt.day_name()

# --- 3. Analysis Section ---
st.subheader("1️⃣ Category Distribution")
category_counts = df['standard_category'].value_counts(normalize=True) * 100
fig1, ax1 = plt.subplots()
ax1.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90,
        colors=['#FF0000', '#555555', '#333333', '#AAAAAA'])
ax1.set_title('Distribution of Trending Video Categories')
st.pyplot(fig1)

st.subheader("2️⃣ Correlation Between Views, Likes, and Comments")
corr = df[['views', 'likes', 'comment_count']].corr()
st.dataframe(corr)

fig2, ax2 = plt.subplots()
sns.scatterplot(x='views', y='likes', data=df, ax=ax2)
ax2.set_title('Views vs Likes')
st.pyplot(fig2)

st.subheader("3️⃣ Average Views by Publish Hour")
hourly_views = df.groupby('publish_hour')['views'].mean().reset_index()
fig3, ax3 = plt.subplots()
sns.lineplot(x='publish_hour', y='views', data=hourly_views, ax=ax3)
ax3.set_title('Average Views by Hour of Day Published')
st.pyplot(fig3)

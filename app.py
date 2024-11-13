import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Calendar Heatmaps for Air Quality Features")

df = pd.read_csv("final.csv")
df = df.drop(df.columns[0], axis=1)  
st.write("Here are the first few rows of your data:")
st.dataframe(df.head())  
df.columns = df.columns.str.strip()

if 'date' in df.columns:
    df['date'] = df['date'].str.strip()

    df['date'] = pd.to_datetime(df['date'], errors='coerce', dayfirst=True)  

    invalid_dates = df[df['date'].isna()]
    if not invalid_dates.empty:
        st.write("Rows with invalid dates:")
        st.dataframe(invalid_dates)  

    df = df.dropna(subset=['date'])

    df.set_index('date', inplace=True)

    features = ['pm25', 'pm10', 'aqi', 'co2', 'voc', 'temp', 'humidity', 'battery', 'viral_index']
    n_features = len(features)
    fig, axes = plt.subplots(n_features, 1, figsize=(30, n_features * 5), constrained_layout=True)  # Increased size

    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    for i, feature in enumerate(features):
        daily_data = df[feature].resample('D').mean()
        calendar_data = daily_data.to_frame().pivot_table(
            index=daily_data.index.to_period("W"), columns=daily_data.index.dayofweek, values=feature
        )

        sns.heatmap(calendar_data, cmap='coolwarm', annot=True, fmt=".1f", 
                    cbar_kws={'label': f'Average {feature}'}, ax=axes[i])

        axes[i].set_title(f'Calendar Heatmap of Daily Average {feature}')
        axes[i].set_xlabel('Day of the Week')
        axes[i].set_ylabel('Week')

        axes[i].set_xticklabels(day_names, rotation=45)

    st.pyplot(fig)

else:
    st.error("The 'date' column is missing in your CSV file.")

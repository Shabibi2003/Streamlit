import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Calendar Heatmaps for Air Quality Features")

# Load data
df = pd.read_csv("final.csv")
df = df.drop(df.columns[0], axis=1)  # Drop the first column if it's index or unwanted data
st.write("Here are the first few rows of your data:")
st.dataframe(df.head())  
df.columns = df.columns.str.strip()

if 'date' in df.columns:
    # Clean and format the 'date' column
    df['date'] = df['date'].str.strip()
    df['date'] = pd.to_datetime(df['date'], errors='coerce', dayfirst=True)  

    # Handle invalid dates
    invalid_dates = df[df['date'].isna()]
    if not invalid_dates.empty:
        st.write("Rows with invalid dates:")
        st.dataframe(invalid_dates)  

    df = df.dropna(subset=['date'])

    df.set_index('date', inplace=True)

    # List of features to plot
    features = ['pm25', 'pm10', 'aqi', 'co2', 'voc', 'temp', 'humidity', 'battery', 'viral_index']
    n_features = len(features)
    
    # Increase the figure size to ensure the calendar is large enough
    fig, axes = plt.subplots(n_features, 1, figsize=(50, n_features * 8), constrained_layout=True)  # Larger size

    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    for i, feature in enumerate(features):
        # Resample to daily mean values
        daily_data = df[feature].resample('D').mean()

        # Pivot data for calendar layout
        calendar_data = daily_data.to_frame().pivot_table(
            index=daily_data.index.to_period("W"), 
            columns=daily_data.index.dayofweek, 
            values=feature
        )

        # Create heatmap
        sns.heatmap(calendar_data, cmap='coolwarm', annot=True, fmt=".1f", 
                    annot_kws={'size': 14},  # Increase annotation size for better readability
                    cbar_kws={'label': f'Average {feature}', 'shrink': 0.7},  # Adjust colorbar size
                    ax=axes[i])

        # Set titles and labels with larger font sizes
        axes[i].set_title(f'Calendar Heatmap of Daily Average {feature}', fontsize=18)
        axes[i].set_xlabel('Day of the Week', fontsize=16)
        axes[i].set_ylabel('Week', fontsize=16)

        axes[i].set_xticklabels(day_names, rotation=45, fontsize=14)  # Set x-axis labels with larger font

    st.pyplot(fig)

else:
    st.error("The 'date' column is missing in your CSV file.")

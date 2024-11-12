import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Title of the Streamlit app
st.title("Calendar Heatmaps for Air Quality Features")

# Path to the CSV file (static file path)
csv_file_path = "https://raw.githubusercontent.com/yourusername/yourrepo/main/final.csv"  # Adjust path or URL

# Read the CSV into a DataFrame
df = pd.read_csv(csv_file_path)

# Display first few rows to understand the structure of the CSV file
st.write("Here are the first few rows of your data:")
st.dataframe(df.head())  # Display the first few rows of the DataFrame in Streamlit UI

# Check if 'date' column exists
if 'date' in df.columns:
    # Attempt to convert 'date' to datetime, handle errors gracefully
    df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Invalid dates will become NaT

    # Check for missing values after conversion
    if df['date'].isna().sum() > 0:
        st.warning(f"There are {df['date'].isna().sum()} invalid date entries that were coerced to NaT.")

    # Drop rows where 'date' is NaT after coercion (if necessary)
    df = df.dropna(subset=['date'])

    # Set the 'date' column as the index
    df.set_index('date', inplace=True)

    # List of features to plot
    features = ['pm25', 'pm10', 'aqi', 'co2', 'voc', 'temp', 'humidity', 'battery', 'viral_index']

    # Set up the subplot grid
    n_features = len(features)
    fig, axes = plt.subplots(n_features, 1, figsize=(12, n_features * 3), constrained_layout=True)

    for i, feature in enumerate(features):
        # Resample and reshape the data for the current feature
        daily_data = df[feature].resample('D').mean()
        calendar_data = daily_data.to_frame().pivot_table(
            index=daily_data.index.to_period("W"), columns=daily_data.index.dayofweek, values=feature
        )

        # Plot the heatmap for the feature
        sns.heatmap(calendar_data, cmap='coolwarm', annot=True, fmt=".1f", 
                    cbar_kws={'label': f'Average {feature}'}, ax=axes[i])

        # Set the title and labels for each subplot
        axes[i].set_title(f'Calendar Heatmap of Daily Average {feature}')
        axes[i].set_xlabel('Day of the Week (0=Monday)')
        axes[i].set_ylabel('Week')

    # Display the calendar heatmaps using Streamlit's pyplot function
    st.pyplot(fig)

else:
    st.error("The 'date' column is missing in your CSV file.")

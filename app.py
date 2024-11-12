import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Title of the Streamlit app
st.title("Calendar Heatmaps for Air Quality Features")

# Path to the CSV file (static file path)
csv_file_path = "final.csv"  # Adjust this path as per your file location

# Read the CSV into a DataFrame
df = pd.read_csv(csv_file_path)

# Drop the first column (which seems like an index or unnecessary column)
df = df.drop(df.columns[0], axis=1)

# Convert the 'date' column to datetime
df['date'] = pd.to_datetime(df['date'])
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

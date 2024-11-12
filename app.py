import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set up the Streamlit title and description
st.title("Air Quality Data Visualization")

st.write("""
    This app displays calendar heatmaps for various air quality features. 
    The data is loaded directly from a pre-defined CSV file.
""")

# Load the data from a predefined CSV file path (adjust this path to where your CSV file is stored)
df = pd.read_csv('final.csv')

# Ensure the 'date' column exists and is in correct datetime format
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Convert to datetime, invalid entries will be NaT
    df = df.dropna(subset=['date'])  # Remove rows with invalid date entries
else:
    st.error("The 'date' column does not exist in the dataset.")
    st.stop()

# Set 'date' as the index
df.set_index('date', inplace=True)

# Define features for visualization
features = ['pm25', 'pm10', 'aqi', 'co2', 'voc', 'temp', 'humidity', 'battery', 'viral_index']

# Ensure the features exist in the dataset
missing_features = [feature for feature in features if feature not in df.columns]
if missing_features:
    st.error(f"These features are missing in the dataset: {', '.join(missing_features)}")
    st.stop()

# Set up the subplot grid
n_features = len(features)
fig, axes = plt.subplots(n_features, 1, figsize=(12, n_features * 3), constrained_layout=True)

# Weekday labels
weekday_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

for i, feature in enumerate(features):
    # Resample and reshape the data for the current feature
    daily_data = df[feature].resample('D').mean()

    # Reindex the data to ensure all days are present in the month, even if some days have missing data
    all_days = pd.date_range(start=daily_data.index.min(), end=daily_data.index.max(), freq='D')
    daily_data = daily_data.reindex(all_days)

    # Pivot the data to a calendar format
    calendar_data = daily_data.to_frame().pivot_table(
        index=daily_data.index.to_period("W"),  # Group by week
        columns=daily_data.index.dayofweek,     # Columns for days of the week (0=Monday)
        values=feature,                          # Values for the feature
        aggfunc='mean'                           # Use mean for aggregation
    )

    # Plot the heatmap for the feature
    sns.heatmap(calendar_data, cmap='coolwarm', annot=True, fmt=".1f", 
                cbar_kws={'label': f'Average {feature}'}, ax=axes[i], 
                xticklabels=weekday_labels, annot_kws={'size': 10, 'weight': 'bold'}, 
                cbar=True, linewidths=0.5)

    # Set the title and labels for each subplot
    axes[i].set_title(f'Calendar Heatmap of Daily Average {feature}')
    axes[i].set_xlabel('Day of the Week', fontsize=12)
    axes[i].set_ylabel('Week', fontsize=12)

# Overall title
plt.suptitle('Calendar Heatmaps for All Features', fontsize=16)

# Display the heatmaps in Streamlit
st.pyplot(fig)

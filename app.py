import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Title of the Streamlit app
st.title("Calendar Heatmaps for Air Quality Features")

# Read the CSV into a DataFrame
df = pd.read_csv("final.csv")

# Display first few rows to understand the structure of the CSV file
st.write("Here are the first few rows of your data:")
st.dataframe(df.head())  # Display the first few rows of the DataFrame in Streamlit UI

# Strip any leading/trailing spaces from the column names (in case there are any)
df.columns = df.columns.str.strip()

# Check if 'date' column exists
if 'date' in df.columns:
    # Strip any extra spaces from the date column, just in case
    df['date'] = df['date'].str.strip()

    # Attempt to convert 'date' to datetime with error handling
    df['date'] = pd.to_datetime(df['date'], errors='coerce', dayfirst=True)  # dayfirst=True for DD/MM/YYYY format

    # Check for missing values after conversion
    invalid_dates = df[df['date'].isna()]
    if not invalid_dates.empty:
        st.write("Rows with invalid dates:")
        st.dataframe(invalid_dates)  # Show the rows with invalid date values

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

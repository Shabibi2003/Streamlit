import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_calendar_heatmaps(df):
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

    plt.suptitle('Calendar Heatmaps for All Features', fontsize=16)
    st.pyplot(fig)

# Streamlit app interface
def main():
    st.title('Calendar Heatmap for Air Quality Features')

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        # Read the data
        df = pd.read_csv(uploaded_file, parse_dates=True, index_col=0)

        # Assuming the 'timestamp' column is the index
        if 'timestamp' not in df.columns:
            st.error("The CSV file must have a 'timestamp' column.")
            return
        
        # Convert the index to datetime (if it's not already)
        df.index = pd.to_datetime(df.index)

        # Check if all the required features exist in the dataframe
        missing_features = [feature for feature in ['pm25', 'pm10', 'aqi', 'co2', 'voc', 'temp', 'humidity', 'battery', 'viral_index'] if feature not in df.columns]
        if missing_features:
            st.error(f"Missing columns: {', '.join(missing_features)}")
            return
        
        # Plot the heatmaps
        plot_calendar_heatmaps(df)

if __name__ == "__main__":
    main()

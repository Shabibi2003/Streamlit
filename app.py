import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import calendar

# Load data
df = pd.read_csv("final.csv")
df = df.drop(columns=[df.columns[0]])  # Drop the first column if it's an index or unwanted column

# Ensure 'date' column exists and is in correct datetime format
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Convert to datetime, invalid entries will be NaT
    df = df.dropna(subset=['date'])  # Remove rows with invalid date entries
else:
    st.error("The 'date' column does not exist in the dataset.")
    st.stop()

df.set_index('date', inplace=True)

# Show the raw dataset in Streamlit UI
st.title("Air Quality Data Overview")

# Display the raw data as a table
st.subheader("Raw Data")
st.dataframe(df)

# Print column names for debugging purposes
st.write("Available columns in the dataset:", df.columns)

# Features for visualization (use actual column names in the dataset)
features = ['pm2.5', 'pm10', 'aqi', 'co2', 'voc', 'temp', 'humidity', 'battery', 'viral_index']  # Replaced pm25 with pm2.5

# Automatically select the month and year based on the data
# Here, we just use the first entry in the data to extract the month and year
first_date = df.index.min()
month = first_date.month
year = first_date.year

# Filter data for the selected month and year
filtered_df = df[(df.index.month == month) & (df.index.year == year)]

# Function to create the calendar layout for heatmap
def create_calendar_heatmap(data, month, year, feature):
    # Get the number of days in the selected month
    num_days = calendar.monthrange(year, month)[1]
    
    # Get the starting weekday for the month (e.g., Monday=0, Sunday=6)
    first_day_of_month = calendar.monthrange(year, month)[0]
    
    # Calculate the number of weeks required for the current month
    num_weeks = (num_days + first_day_of_month - 1) // 7 + 1  # We calculate how many full weeks fit into the month
    
    # Create a grid for the calendar, dynamically adjust rows based on the number of weeks
    calendar_grid = np.full((num_weeks, 7), np.nan)  # Use 'num_weeks' instead of hardcoding 6
    
    # Populate the calendar grid with values from the feature
    for day in range(1, num_days + 1):
        # Get data for the current day
        day_data = data[data.index.day == day]
        if not day_data.empty:
            # Get the average value for the feature
            avg_value = day_data[feature].mean()
        else:
            avg_value = np.nan
        
        # Find the corresponding position in the calendar grid
        row = (day + first_day_of_month - 1) // 7  # Determine the week row
        col = (day + first_day_of_month - 1) % 7  # Determine the day column
        
        # Assign the average value to the grid cell
        calendar_grid[row, col] = avg_value
    
    return calendar_grid

# Plot the calendar heatmap for each feature
for feature in features:
    # Check if the feature exists in the dataset
    if feature not in df.columns:
        st.error(f"Feature '{feature}' does not exist in the dataset.")
        continue
    
    # Generate the calendar grid for the current feature
    calendar_grid = create_calendar_heatmap(filtered_df, month, year, feature)
    
    # Create the heatmap plot
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(calendar_grid, cmap='coolwarm', annot=True, fmt=".1f", cbar_kws={'label': feature},
                xticklabels=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                yticklabels=[f'Week {i+1}' for i in range(calendar_grid.shape[0])],  # Adjust week labels dynamically
                ax=ax, square=True, annot_kws={'size': 10, 'weight': 'bold'})

    # Add title and labels
    ax.set_title(f"Calendar Heatmap for {feature} - {calendar.month_name[month]} {year}", fontsize=14)
    ax.set_xlabel('Day of Week', fontsize=12)
    ax.set_ylabel('Week', fontsize=12)
    
    # Display the plot in Streamlit
    st.pyplot(fig)

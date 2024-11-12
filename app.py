import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import calendar

# Load data
df = pd.read_csv("final.csv")
df = df.drop(columns=[df.columns[0]])

# Ensure 'date' column exists and is in correct datetime format
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Convert to datetime, invalid entries will be NaT
    df = df.dropna(subset=['date'])  # Remove rows with invalid date entries
else:
    st.error("The 'date' column does not exist in the dataset.")
    st.stop()

df.set_index('date', inplace=True)

# Features for visualization
features = ['pm25', 'pm10', 'aqi', 'co2', 'voc', 'temp', 'humidity', 'battery', 'viral_index']

# Streamlit app title
st.title("Calendar Heatmap")

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
    
    # Create a grid for the calendar
    calendar_grid = np.full((6, 7), np.nan)  # 6 rows (weeks), 7 columns (days of the week)
    
    # Get the starting weekday for the month (e.g., Monday=0, Sunday=6)
    first_day_of_month = calendar.monthrange(year, month)[0]
    
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
    # Generate the calendar grid for the current feature
    calendar_grid = create_calendar_heatmap(filtered_df, month, year, feature)
    
    # Create the heatmap plot
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(calendar_grid, cmap='coolwarm', annot=True, fmt=".1f", cbar_kws={'label': feature},
                xticklabels=[ 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat','Sun'],
                yticklabels=['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6'],
                ax=ax, square=True, annot_kws={'size': 10, 'weight': 'bold'})

    # Add title and labels
    ax.set_title(f"Calendar Heatmap for {feature} - {calendar.month_name[month]} {year}", fontsize=14)
    ax.set_xlabel('Day of Week', fontsize=12)
    ax.set_ylabel('Week', fontsize=12)
    
    # Display the plot in Streamlit
    st.pyplot(fig)

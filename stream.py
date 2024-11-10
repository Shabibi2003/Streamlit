import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# Database connection
def create_connection():
    conn = sqlite3.connect('expenses.db')
    return conn

# Initialize the database and create table if it doesn't exist
def init_db():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            amount REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Insert data into the database
def insert_expense(date, category, description, amount):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (date, category, description, amount)
        VALUES (?, ?, ?, ?)
    ''', (date, category, description, amount))
    conn.commit()
    conn.close()

# Display data from the database
def view_expenses():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Delete all records in the database
def delete_all_expenses():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM expenses')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

# App UI
st.title("Monthly Expenditure Tracker")

# Sidebar form to add expenses
with st.sidebar.form("expense_form", clear_on_submit=True):
    st.subheader("Add New Expense")
    date = st.date_input("Date", datetime.now())
    category = st.selectbox("Category", ["Food", "Transport", "Rent", "Utilities", "Others"])
    description = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    
    submit_button = st.form_submit_button("Add Expense")

# Handle form submission
if submit_button:
    insert_expense(date.strftime("%Y-%m-%d"), category, description, amount)
    st.success("Expense added successfully!")

# Delete all records button
if st.sidebar.button("Delete All Records"):
    delete_all_expenses()
    st.sidebar.success("All records have been deleted!")

# Display the expenses table
st.subheader("All Expenses")
expenses = view_expenses()

# Convert data to DataFrame
if expenses:
    df = pd.DataFrame(expenses, columns=["ID", "Date", "Category", "Description", "Amount"])
    st.dataframe(df)

    # Display a bar chart of expenses by category
    st.subheader("Expenses by Category")
    expenses_by_category = df.groupby("Category")["Amount"].sum()
    st.bar_chart(expenses_by_category)
    
    # Display a line chart of expenses over time
    st.subheader("Expenses Over Time")
    # Convert 'Date' column to datetime format
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
    
    # Drop rows with invalid dates (if any)
    df = df.dropna(subset=["Date"])
    
    # Group by date and sort for time-series plotting
    expenses_over_time = df.groupby("Date")["Amount"].sum().sort_index()

    if not expenses_over_time.empty:
        # Calculate the total sum of expenses
        total_expense = expenses_over_time.sum()

        # Plot the line chart of expenses over time
        st.line_chart(expenses_over_time)

        # Display total spending below the graph
        st.write(f"**Total Spending:** {total_expense:.2f}")
    else:
        st.write("No data available for the 'Expenses Over Time' chart.")
else:
    st.write("No expenses to display.")

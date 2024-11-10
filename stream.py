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

# Set default values for session state if not already set
if "form_data" not in st.session_state:
    st.session_state.form_data = {
        "date": datetime.now(),
        "category": "Food",
        "description": "",
        "amount": 0.0
    }

# Sidebar form to add expenses
with st.sidebar.form("expense_form"):
    st.subheader("Add New Expense")
    st.session_state.form_data["date"] = st.date_input("Date", st.session_state.form_data["date"])
    st.session_state.form_data["category"] = st.selectbox("Category", ["Food", "Transport", "Rent", "Utilities", "Others"], index=["Food", "Transport", "Rent", "Utilities", "Others"].index(st.session_state.form_data["category"]))
    st.session_state.form_data["description"] = st.text_input("Description", st.session_state.form_data["description"])
    st.session_state.form_data["amount"] = st.number_input("Amount", min_value=0.0, value=st.session_state.form_data["amount"], format="%.2f")
    
    submit_button = st.form_submit_button("Add Expense")
    clear_button = st.form_submit_button("Clear Form")

# Handle form submission
if submit_button:
    insert_expense(st.session_state.form_data["date"].strftime("%Y-%m-%d"), st.session_state.form_data["category"], st.session_state.form_data["description"], st.session_state.form_data["amount"])
    st.success("Expense added successfully!")

# Handle form reset
if clear_button:
    st.session_state.form_data = {
        "date": datetime.now(),
        "category": "Food",
        "description": "",
        "amount": 0.0
    }

# Delete all records button
if st.sidebar.button("Delete All Records"):
    if st.sidebar.checkbox("Confirm Delete"):
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
    df["Date"] = pd.to_datetime(df["Date"])
    expenses_over_time = df.groupby("Date")["Amount"].sum()
    st.line_chart(expenses_over_time)
else:
    st.write("No expenses to display.")

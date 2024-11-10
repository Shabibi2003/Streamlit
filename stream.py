import streamlit as st
import sqlite3
from datetime import datetime

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

# Initialize the database
init_db()

# App UI
st.title("Monthly Expenditure Tracker")

# Sidebar form to add expenses
with st.sidebar.form("expense_form"):
    st.subheader("Add New Expense")
    date = st.date_input("Date", datetime.now())
    category = st.selectbox("Category", ["Food", "Transport", "Rent", "Utilities", "Others"])
    description = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    
    # Submit and Reset buttons
    submit_button = st.form_submit_button("Add Expense")
    reset_button = st.form_submit_button("Reset")

# Handle form submission
if submit_button:
    insert_expense(date.strftime("%Y-%m-%d"), category, description, amount)
    st.success("Expense added successfully!")

# Handle reset button functionality
if reset_button:
    st.experimental_rerun()  # Refresh the app to reset form inputs

# Display the expenses table
st.subheader("All Expenses")
expenses = view_expenses()
for expense in expenses:
    st.write(f"Date: {expense[1]}, Category: {expense[2]}, Description: {expense[3]}, Amount: ${expense[4]:.2f}")

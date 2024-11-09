import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit
# Title of the app
import pip
installed_packages = pip.get_installed_distributions()
for package in installed_packages:
    print(package)

st.title('My First Streamlit App')

# Display some text
st.write("Hello, this is a simple Streamlit application!")

# Create a simple DataFrame
data = pd.DataFrame({
    'x': np.arange(0, 10),
    'y': np.random.rand(10)
})

# Display the DataFrame as a table
st.write(data)

# Create a simple plot
fig, ax = plt.subplots()
ax.plot(data['x'], data['y'], label='Random Data')
ax.set_title('Line plot of Random Data')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.legend()

# Display the plot in the Streamlit app
st.pyplot(fig)

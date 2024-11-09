# import streamlit as s
# import numpy as np
# import pandas as ppyplot as plt
# import streamlitd
# import matplotlib.
# Title of the app
streamlit
numpy 
pandas
matplotlib

streamlit.title('My First Streamlit App')

# Display some text
streamlit.write("Hello, this is a simple Streamlit application!")

# Create a simple DataFrame
data = pandas.DataFrame({
    'x': numpy.arange(0, 10),
    'y': numpy.random.rand(10)
})

# Display the DataFrame as a table
streamlit.write(data)

# Create a simple plot
fig, ax = matplotlib.subplots()
ax.plot(data['x'], data['y'], label='Random Data')
ax.set_title('Line plot of Random Data')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.legend()

# Display the plot in the Streamlit app
streamlit.pyplot(fig)

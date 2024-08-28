import os
import streamlit as st

# Retrieve the secret from the environment variable
super_quiet_value = os.getenv("SUPER_QUIET")

# Display the value in Streamlit
st.write(f"The secret value is: {super_quiet_value}")

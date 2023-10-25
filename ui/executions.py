# streamlit_app.py
import streamlit as st
from models.core import Session, Execution
import pandas as pd

# Fetch Executions from the database
session = Session()
executions = session.query(Execution).all()
session.close()

# Convert Executions to a Pandas DataFrame for easier display
data = [
    {"id": execution.id, "date_executed": execution.date_executed}
    for execution in executions
]
df = pd.DataFrame(data)

# Streamlit UI
st.title("Executions")
st.table(df)

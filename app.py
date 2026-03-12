import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Smart Appliance Behavioral Monitoring Dashboard")

# Appliance selector
appliance = st.selectbox(
    "Select Appliance",
    ["Refrigerator", "Air Conditioner"]
)

# Load dataset
if appliance == "Refrigerator":
    df = pd.read_csv("fridge_results.csv")
else:
    df = pd.read_csv("ac_results.csv")

# Day selector
selected_day = st.slider(
    "Select Day",
    int(df["Day"].min()),
    int(df["Day"].max()),
    0
)

# Filter selected row
day_data = df[df["Day"] == selected_day]

st.subheader("Appliance Status")

if not day_data.empty:

    error = day_data["Reconstruction_Error"].values[0]
    status = day_data["Risk_Status"].values[0]

    st.metric("Risk Status", status)
    st.metric("Reconstruction Error", round(error,6))

else:
    st.write("No data available")

# Graph
st.subheader("Behavior Trend")

fig, ax = plt.subplots()

ax.plot(df["Day"], df["Reconstruction_Error"], label="Reconstruction Error")

ax.set_xlabel("Day")
ax.set_ylabel("Reconstruction Error")

ax.legend()

st.pyplot(fig)

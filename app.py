import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Smart Appliance Behavioral Monitoring Dashboard")

# Appliance selection
appliance = st.selectbox(
    "Select Appliance",
    ["Refrigerator", "Air Conditioner"]
)

# Load correct dataset
if appliance == "Refrigerator":
    df = pd.read_csv("fridge_streamlit_results.csv")
else:
    df = pd.read_csv("ac_results.csv")

# Check required columns
required_cols = ["Day","Reconstruction_Error","Risk_Status"]
for col in required_cols:
    if col not in df.columns:
        st.error(f"Missing column: {col}")
        st.stop()

# Day selector
selected_day = st.slider(
    "Select Day",
    int(df["Day"].min()),
    int(df["Day"].max()),
    int(df["Day"].min())
)

# Get selected day data
day_data = df[df["Day"] == selected_day]

st.subheader("Appliance Status")

if not day_data.empty:

    error = day_data["Reconstruction_Error"].values[0]
    status = day_data["Risk_Status"].values[0]

    st.metric("Risk Status", status)
    st.metric("Reconstruction Error", round(error,6))

    if status == "High Risk":
        st.error("High Risk Behavior Detected")
    elif status == "Warning":
        st.warning("Appliance Behavior Warning")
    else:
        st.success("Appliance Operating Normally")

else:
    st.write("No data available")

# Trend graph
st.subheader("Behavior Trend")

fig, ax = plt.subplots()

ax.plot(df["Day"], df["Reconstruction_Error"], label="Reconstruction Error")

ax.set_xlabel("Day")
ax.set_ylabel("Reconstruction Error")

ax.legend()

st.pyplot(fig)

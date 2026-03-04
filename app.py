import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Appliance Health Monitoring Dashboard")

st.header("Fridge Monitoring")

fridge = pd.read_csv("fridge_streamlit_results.csv")

st.write(fridge)

fig1, ax1 = plt.subplots()
ax1.plot(fridge["Reconstruction_Error"])
ax1.set_title("Fridge Reconstruction Error")
ax1.set_xlabel("Day")
ax1.set_ylabel("Error")
st.pyplot(fig1)


st.header("AC Monitoring")

ac = pd.read_csv("ac_streamlit_results.csv")

st.write(ac)

fig2, ax2 = plt.subplots()
ax2.plot(ac["Reconstruction_Error"])
ax2.set_title("AC Reconstruction Error")
ax2.set_xlabel("Day")
ax2.set_ylabel("Error")
st.pyplot(fig2)

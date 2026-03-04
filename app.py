import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Appliance Health Monitoring Dashboard")

st.header("Upload Appliance Data")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.subheader("Data Preview")
    st.write(df)

    if "Reconstruction_Error" in df.columns:

        st.subheader("Reconstruction Error Graph")

        fig, ax = plt.subplots()
        ax.plot(df["Reconstruction_Error"])
        ax.set_xlabel("Day")
        ax.set_ylabel("Error")
        ax.set_title("Appliance Reconstruction Error")

        st.pyplot(fig)

        if "Risk_Status" in df.columns:
            st.subheader("Risk Status")
            st.write(df[["Day","Risk_Status"]])

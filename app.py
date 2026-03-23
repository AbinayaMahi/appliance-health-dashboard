# app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Appliance Health Monitor", layout="wide")
st.title("Smart Appliance Behavioral Health Dashboard")

appliance = st.selectbox("Select Appliance", ["Refrigerator", "Air Conditioner"])
fname = "fridge_results.csv" if appliance == "Refrigerator" else "ac_results.csv"
df = pd.read_csv(fname)
df['date'] = pd.to_datetime(df['date'])

# ── Row 1: gauge + summary metrics ───────────────────────────
col1, col2, col3, col4 = st.columns(4)
latest = df.iloc[-1]

fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=float(latest['Health_Score']),
    gauge={
        'axis': {'range': [0, 100]},
        'steps': [
            {'range': [0,  40], 'color': '#FFCCCC'},
            {'range': [40, 70], 'color': '#FFF3CC'},
            {'range': [70,100], 'color': '#CCFFCC'}
        ],
        'threshold': {'value': 40, 'line': {'color': 'red', 'width': 3}}
    },
    title={'text': "Current Health Score"}
))
fig_gauge.update_layout(height=250, margin=dict(t=40,b=10,l=10,r=10))
col1.plotly_chart(fig_gauge, use_container_width=True)

col2.metric("Risk Status",     latest['Risk_Status'])
col3.metric("Autoencoder signal", f"{latest['err_norm']*100:.0f}%")
col4.metric("Trend drift signal", f"{latest['slope_norm']*100:.0f}%")

# ── Row 2: 90-day health trend ────────────────────────────────
st.subheader("Health Score Trend (last 90 days)")
recent = df.tail(90)
color_map = {'Normal': 'green', 'Warning': 'orange', 'High Risk': 'red'}
fig_trend = px.scatter(recent, x='date', y='Health_Score',
                       color='Risk_Status',
                       color_discrete_map=color_map)
fig_trend.add_scatter(x=recent['date'], y=recent['Health_Score'],
                      mode='lines', line=dict(color='gray', width=1),
                      showlegend=False)
fig_trend.update_layout(height=280)
st.plotly_chart(fig_trend, use_container_width=True)

# ── Row 3: CDI component breakdown ───────────────────────────
st.subheader("CDI Component Contribution Over Time")
fig_area = go.Figure()
fig_area.add_trace(go.Scatter(x=df['date'], y=df['err_norm']*50,
    fill='tozeroy', name='Autoencoder error (50%)', line=dict(color='#7F77DD')))
fig_area.add_trace(go.Scatter(x=df['date'], y=df['slope_norm']*30,
    fill='tozeroy', name='Trend drift (30%)', line=dict(color='#1D9E75')))
fig_area.add_trace(go.Scatter(x=df['date'], y=df['z_norm']*20,
    fill='tozeroy', name='Z-deviation (20%)', line=dict(color='#EF9F27')))
fig_area.update_layout(height=280)
st.plotly_chart(fig_area, use_container_width=True)

# ── Row 4: day-by-day table ───────────────────────────────────
st.subheader("Daily Risk Log")
st.dataframe(df[['date','Health_Score','Risk_Status',
                 'Reconstruction_Error']].tail(30).sort_values('date', ascending=False),
             use_container_width=True)

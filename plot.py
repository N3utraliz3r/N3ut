import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- Load CSV ---
df = pd.read_csv("nifty50_1min_combined_processed.csv", parse_dates=['datetime'])
df.set_index('datetime', inplace=True)

# --- Optional: filter to full range or subset ---
df = df.sort_index()
df = df.loc['2020':]  # Show data from 2020 onward

# --- Calculate Donchian Channels ---
dc_length = 20
df['dc_upper'] = df['high'].rolling(dc_length).max().ffill()
df['dc_lower'] = df['low'].rolling(dc_length).min().ffill()

# --- Sample signals (Replace with real logic) ---
df['entry_long'] = ((df['close'] > df['dc_upper']) & (df['volume'] > 0))  # dummy
df['exit_long'] = ((df['close'] < df['dc_lower']) & (df['volume'] > 0))  # dummy

# --- Plot ---
fig = go.Figure()

# Candles
fig.add_trace(go.Candlestick(
    x=df.index,
    open=df['open'], high=df['high'],
    low=df['low'], close=df['close'],
    name="Candles"
))

# DC Bands
fig.add_trace(go.Scatter(
    x=df.index, y=df['dc_upper'], mode='lines',
    line=dict(color='green', width=1),
    name="DC Upper"
))
fig.add_trace(go.Scatter(
    x=df.index, y=df['dc_lower'], mode='lines',
    line=dict(color='red', width=1),
    name="DC Lower"
))

# Entry Signal
fig.add_trace(go.Scatter(
    x=df[df['entry_long']].index,
    y=df[df['entry_long']]['low'] * 0.998,
    mode='markers',
    marker=dict(symbol='arrow-up', color='lime', size=12),
    name="Entry Long"
))

# Exit Signal
fig.add_trace(go.Scatter(
    x=df[df['exit_long']].index,
    y=df[df['exit_long']]['high'] * 1.002,
    mode='markers',
    marker=dict(symbol='arrow-down', color='red', size=12),
    name="Exit Long"
))

fig.update_layout(
    title="Candlestick + Donchian + Signals",
    xaxis_title="Time",
    yaxis_title="Price",
    template="plotly_dark",
    xaxis_rangeslider_visible=False,
    height=800,
)

# --- Streamlit Display ---
st.plotly_chart(fig, use_container_width=True)

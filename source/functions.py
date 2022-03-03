import pandas as pd
import plotly.graph_objects as go

def plot_candle(df):
    fig = go.Figure(data=[go.Candlestick(x=pd.to_datetime(df['Date']),
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'])])
    fig.update(layout_yaxis_range = [0,max(df['High'] *1.1)])
    return fig



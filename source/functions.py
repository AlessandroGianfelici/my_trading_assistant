import pandas as pd
import plotly.graph_objects as go
import talib
import yaml
from talib import MA_Type
from toolz.functoolz import juxt


def load_yaml(filename: str) -> dict:
    """
    Utility function to load a yaml file into a pyhon dict
    Parameters:
    - filename: str -> fullpath of the yaml file
    """
    assert filename.endswith("yaml") or filename.endswith(
        "yml"
    ), "Not a yaml extention!"
    with open(filename, "r", encoding="utf-8") as handler:
        return yaml.load(handler, Loader=yaml.FullLoader)


def simple_moving_average(price_data):
    return go.Scatter(
        x=pd.to_datetime(price_data["Date"]),
        y=talib.SMA(price_data["Close"]),
        name="SMA",
        yaxis="y1",
        showlegend=True,
    )


def upper_bollinger_band(price_data, matype=MA_Type.T3):
    upper, middle, lower = talib.BBANDS(price_data["Close"], matype=matype)
    return go.Scatter(
        x=pd.to_datetime(price_data["Date"]),
        y=upper,
        name="Bollinger band (upper)",
        yaxis="y1",
        showlegend=True,
    )


def middle_bollinger_band(price_data, matype=MA_Type.T3):
    upper, middle, lower = talib.BBANDS(price_data["Close"], matype=matype)
    return go.Scatter(
        x=pd.to_datetime(price_data["Date"]),
        y=middle,
        name="Bollinger band (middle)",
        yaxis="y1",
        showlegend=True,
    )


def lower_bollinger_band(price_data, matype=MA_Type.T3):
    upper, middle, lower = talib.BBANDS(price_data["Close"], matype=matype)
    return go.Scatter(
        x=pd.to_datetime(price_data["Date"]),
        y=lower,
        name="Bollinger band (lower)",
        yaxis="y1",
        showlegend=True,
    )


def hilbert_instantaneous_trendline(price_data):
    return go.Scatter(
        x=pd.to_datetime(price_data["Date"]),
        y=talib.HT_TRENDLINE(price_data["Close"]),
        name="Hilbert Transform - Instantaneous Trendline",
        yaxis="y1",
        showlegend=True,
    )


def plot_candle(price_data, indicators=[]):

    layout = go.Layout(
        yaxis=dict(title="Price"),
        yaxis2=dict(title="Volume", overlaying="y", side="right"),
    )

    technical_indicators = juxt(indicators)(price_data)

    prices_date = pd.to_datetime(price_data["Date"])

    fig = go.Figure(
        layout=layout,
        data=[
            go.Candlestick(
                x=prices_date,
                open=price_data["Open"],
                high=price_data["High"],
                low=price_data["Low"],
                close=price_data["Close"],
                yaxis="y1",
                name="Price",
            ),
            go.Bar(
                x=prices_date,
                y=price_data["Volume"],
                name="Volume",
                marker={"color": "blue"},
                yaxis="y2",
            ),
        ]
        + list(technical_indicators),
    )

    fig.update(layout_yaxis_range=[0, max(price_data["High"] * 1.1)])
    return fig

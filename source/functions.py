import pandas as pd
import plotly.graph_objects as go
import yaml


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


def plot_candle(price_data):
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=pd.to_datetime(price_data["Date"]),
                open=price_data["Open"],
                high=price_data["High"],
                low=price_data["Low"],
                close=price_data["Close"],
            )
        ]
    )
    fig.update(layout_yaxis_range=[0, max(price_data["High"] * 1.1)])
    return fig

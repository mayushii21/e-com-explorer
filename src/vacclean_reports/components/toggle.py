import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import html


def toggle():
    return dbc.Row(
        [
            dbc.Col(html.Span("Stacked"), width=3),
            dbc.Col(daq.ToggleSwitch(id="toggle", value=False), width=3),
            dbc.Col(html.Span("Grouped"), width=3),
        ],
        justify="center",
    )

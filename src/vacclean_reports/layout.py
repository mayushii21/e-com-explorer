import dash_bootstrap_components as dbc

from vacclean_reports.app import app
from vacclean_reports.components.main_chart import (
    agg_dd,
    element_dd,
    main_chart,
    metric_radio,
)
from vacclean_reports.components.themes import theme_changer

# Pool (combine) the layout
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(agg_dd(), width=2),
                dbc.Col(metric_radio(), width=6),
                dbc.Col(element_dd(), width=4),
            ],
            align="center",
            # justify="between",
        ),
        dbc.Row(dbc.Col(main_chart())),
        dbc.Row(
            dbc.Col(theme_changer, width=2),
        ),
    ],
    fluid=True,
    class_name="dbc",  # element colors
    # style={"height": "100%", "width": "100%", "margin": 0, "overflow": "hidden"},
)

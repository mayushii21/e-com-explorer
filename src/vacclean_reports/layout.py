import dash_bootstrap_components as dbc
from dash import html

from vacclean_reports.app import app
from vacclean_reports.components.main_chart import (
    agg_dd,
    element_dd,
    main_chart,
    metric_radio,
)
from vacclean_reports.components.themes import theme_changer
from vacclean_reports.components.top_items import table_info, top_items_chart

# Pool (combine) the layout
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(html.H1("Wildberries Dashboard", style={"textAlign": "center"}))
        ),
        dbc.Row(
            [
                dbc.Col(agg_dd(), width=2),
                dbc.Col(metric_radio(), width=6),
                dbc.Col(element_dd(), width=4),
            ],
            align="center",
            # justify="between",
            style={
                "position": "-webkit-sticky",
                # "position": "sticky",
                "top": 0,
            },
        ),
        dbc.Row(dbc.Col(main_chart())),
        dbc.Row(dbc.Col(top_items_chart())),
        dbc.Row(
            dbc.Col(
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            table_info(),
                            title="Таблица топ товаров",
                        ),
                    ],
                    start_collapsed=True,
                )
            )
        ),
        dbc.Row(
            dbc.Col(theme_changer, width=2),
        ),
    ],
    fluid=True,
    class_name="dbc",  # element colors
    # style={"height": "100%", "width": "100%", "margin": 0, "overflow": "hidden"},
)

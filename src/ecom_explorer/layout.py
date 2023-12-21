import dash_bootstrap_components as dbc
from dash import html

from ecom_explorer.app import app
from ecom_explorer.components.brands import top_brands_chart
from ecom_explorer.components.main_chart import (
    agg_dd,
    element_dd,
    main_chart,
    metric_radio,
)
from ecom_explorer.components.sellers import top_sellers_chart, top_sellers_n_sku_chart
from ecom_explorer.components.themes import theme_changer
from ecom_explorer.components.toggle import toggle
from ecom_explorer.components.top_items import table_info, top_items_chart

# Pool (combine) the layout
app.layout = dbc.Container(
    [
        # Title row
        dbc.Row(
            dbc.Col(html.H1("Wildberries Dashboard", style={"textAlign": "center"}))
        ),
        # Sticky row with selection options
        dbc.Row(
            [
                dbc.Col(agg_dd(), width=2),
                dbc.Col(metric_radio(), width=6),
                dbc.Col(element_dd(), width=4),
            ],
            align="center",
            style={"position": "sticky", "top": 0, "zIndex": 999},
            className="bg-body",  # remove transparency of row
        ),
        # First chart
        dbc.Row(dbc.Col(main_chart())),
        # Chart with top items
        dbc.Row(dbc.Col(top_items_chart())),
        # Table in dropdown accordion
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
        # Sunburst and horizontal bar chart for top sellers and their items
        dbc.Row(
            [
                dbc.Col(top_sellers_n_sku_chart(), width=6),
                dbc.Col(top_sellers_chart(), width=6),
            ]
        ),
        # Top brands chart
        dbc.Row(dbc.Col(top_brands_chart())),
        # Theme changer button
        dbc.Row(
            [
                dbc.Col(theme_changer, width=2),
                dbc.Col(toggle(), width=3),
            ],
            justify="between",
            style={"position": "sticky", "bottom": 0, "zIndex": 999},
        ),
    ],
    fluid=True,
    class_name="dbc",  # element colors
)

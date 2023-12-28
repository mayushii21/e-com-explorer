import plotly.express as px
from dash import dcc
from dash.dependencies import Input, Output, State
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url

from ecom_explorer.components.decorators import callback, data_access


# Aggregation method
def agg_dd():
    return dcc.Dropdown(
        id="agg-dd",
        options=[
            {"label": "Общ. (сумма)", "value": "sum"},
            {"label": "Среднее", "value": "mean"},
            {"label": "Медиана", "value": "median"},
        ],
        value="mean",
        clearable=False,
    )


# Element selection
@data_access
def element_dd(data):
    # Get latest unique sku, name pairs sorted by name
    temp = (
        data[["SKU", "Название"]]
        .drop_duplicates(subset="SKU", keep="last")
        .sort_values(by="Название")
    )
    return dcc.Dropdown(
        id="element-dd",
        # Generate options with "all" as the first value
        options=[
            {"label": "Все", "value": "all"},
        ]
        + [
            {"label": name, "value": sku}
            for sku, name in zip(temp["SKU"], temp["Название"])
        ],
        value="all",
        clearable=False,
    )


# Enable/disable Multi-Select Dropdown
@callback(
    Output("element-dd", "multi"),
    Output("element-dd", "value"),
    Input("element-dd", "value"),
)
def update_element_dd(val):
    if (isinstance(val, (list, str)) and "all" in val) or not val:
        return False, "all"
    else:
        return True, val


# Metric selection
def metric_radio():
    return dcc.RadioItems(
        value="Revenue",
        id="metric-radio",
        inline=True,
        labelStyle={
            "cursor": "pointer",
            "marginLeft": "3%",
            "marginRight": "3%",
        },
        inputStyle={"marginRight": "10px"},
        style={"textAlign": "center"},
    )


# Disable price option when aggregation method is sum
@callback(
    Output("metric-radio", "options"),
    Output("metric-radio", "value"),
    Input("agg-dd", "value"),
    State("metric-radio", "value"),
)
def update_metric_radio(agg_m, val):
    if agg_m == "sum":
        return [
            {"label": "Revenue", "value": "Выручка"},
            {"label": "Sales", "value": "Продажи"},
            {"label": "Price", "value": "Цена", "disabled": True},
            {"label": "Demand & Stock", "value": "Запросы Остатки"},
        ], val if val != "Price" else "Revenue"
    else:
        return [
            {"label": "Revenue", "value": "Выручка"},
            {"label": "Sales", "value": "Продажи"},
            {"label": "Price", "value": "Цена"},
            {"label": "Demand & Stock", "value": "Запросы Остатки"},
        ], val


def main_chart():
    return dcc.Graph(
        id="main-chart",
        responsive=True,
        style={"height": "85vh"},
    )


# Update main chart
@callback(
    Output("main-chart", "figure"),
    Input("metric-radio", "value"),
    Input("agg-dd", "value"),
    Input("element-dd", "value"),
    Input(ThemeChangerAIO.ids.radio("theme"), "value"),
)
@data_access
def update_main_chart(
    df,
    metric,
    agg_m,
    elements,
    theme,
):
    # Handle double metric
    metrics = metric.split()
    # Apply proper formatting
    main_data = (
        metric + "/день" if len(metrics) == 1 else [m + "/день" for m in metrics]
    )
    # Generate filter based on element selection
    if elements == "all":
        filt = slice(None)
    elif isinstance(elements, list):
        filt = df.SKU.isin(elements)
    else:
        filt = df.SKU.isin([elements])
    # Plot chart with applied filter for chosen metric
    fig = px.line(
        df[filt].groupby("Дата", as_index=False)[main_data].agg(agg_m),
        x="Дата",
        y=main_data,
        labels={"value": ""},
        template=template_from_url(theme),
    )
    # Remove excessive margins
    fig.update_layout(
        margin=dict(
            l=0,
            r=0,
            b=0,
        )
    )

    return fig

import pandas as pd
import plotly.express as px
from dash import dash_table, dcc
from dash.dependencies import Input, Output, State
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url

from vacclean_reports.components.decorators import callback, data_access


def top_items_chart():
    return dcc.Graph(
        id="top-items-chart",
        # config={"modeBarButtonsToRemove": ["select2d", "lasso2d", "zoom"]},
        responsive=True,
        style={"height": "90vh"},
    )


# This DataTable contains monthly metrics for all items
def table_info():
    return dash_table.DataTable(
        id="items-table",
        # style_cell={
        #     "font_size": "12px",
        #     "textAlign": "right",
        #     "padding-right": "7px",
        # },
        # style_cell_conditional=[
        #     {
        #         "if": {"column_id": "symbol"},
        #         "textAlign": "left",
        #         "padding-left": "7px",
        #     },
        #     {"if": {"column_id": ["price", "90-day corr"]}, "width": "30%"},
        # ],
        # style_header={"backgroundColor": "rgba(0,0,0,0)"},
        # style_data={"backgroundColor": "rgba(0,0,0,0)"},
        # style_table={
        #     # "height": "calc(100vh)",
        #     "height": "calc(100vh - 2em - (10.6em * 1.5) - 1.7em - 300px)",
        #     "overflowY": "auto",
        # },
        style_as_list_view=True,
    )


# Update top items chart
@callback(
    Output("top-items-chart", "figure"),
    Output("items-table", "data"),
    Input("metric-radio", "value"),
    Input("agg-dd", "value"),
    Input(ThemeChangerAIO.ids.radio("theme"), "value"),
)
@data_access
def update_items_chart_n_table(
    df,
    metric,
    agg_m,
    theme,
):
    # # Handle double metric
    # metrics = metric.split()
    # # Apply proper formatting
    # main_data = (
    #     metric + "/день" if len(metrics) == 1 else [m + "/день" for m in metrics]
    # )

    # Group by month and sku
    prep = df.groupby(["SKU", pd.Grouper(key="Дата", freq="M")], as_index=False)[
        "Продажи/день"
    ].sum()
    # Pivot months to columns
    prep = prep.pivot(index="SKU", columns="Дата", values="Продажи/день")
    # Set month names
    months = ["Aug.", "Sept.", "Oct."]
    prep.columns = months
    # Calculate totals and sort
    prep["Total"] = prep.sum(axis=1)
    prep.sort_values(by="Total", ascending=False, inplace=True)
    prep.reset_index(inplace=True)
    # Add item names
    prep = prep.join(
        df[["SKU", "Название"]]
        .drop_duplicates(subset="SKU", keep="last")
        .set_index("SKU"),
        on="SKU",
        how="left",
    )
    # To string for plotting
    prep["SKU"] = prep.SKU.astype(str)
    # Plot
    fig = px.bar(
        prep[prep.Total != 0],
        x=prep.loc[prep.Total != 0, "SKU"],
        y=months,
        labels={"value": "Продаж", "x": "SKU"},
        title="Сумма продаж по товарам",
        barmode="stack",
        template=template_from_url(theme),
    )
    fig.update_layout(legend_title="Months")

    return fig, prep[[prep.columns[-1]] + list(prep.columns[:-1])].to_dict("records")

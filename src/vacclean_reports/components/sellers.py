import pandas as pd
import plotly.express as px
from dash import dcc
from dash.dependencies import Input, Output, State
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url

from vacclean_reports.components.decorators import callback, data_access


def top_sellers_chart():
    return dcc.Graph(
        id="top-sellers-chart",
        # config={"modeBarButtonsToRemove": ["select2d", "lasso2d", "zoom"]},
        # responsive=True,
    )


def top_sellers_n_sku_chart():
    return dcc.Graph(
        id="top-sellers-n-sku-chart",
        # config={"modeBarButtonsToRemove": ["select2d", "lasso2d", "zoom"]},
        # responsive=True,
    )


# Update top sellers chart
@callback(
    Output("top-sellers-chart", "figure"),
    Input("metric-radio", "value"),
    Input("agg-dd", "value"),
    Input(ThemeChangerAIO.ids.radio("theme"), "value"),
)
@data_access
def update_sellers_chart(
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

    # Group by seller and month
    prep = df.groupby(["Продавец", pd.Grouper(key="Дата", freq="M")], as_index=False)[
        "Продажи/день"
    ].sum()
    # Pivot months to columns
    prep = prep.pivot(index="Продавец", columns="Дата", values="Продажи/день")
    # Set month names
    months = ["Aug.", "Sept.", "Oct."]
    prep.columns = months
    # Calculate totals and sort
    prep["Total"] = prep.sum(axis=1)
    prep.sort_values(by="Total", inplace=True)
    prep.reset_index(inplace=True)
    # Plot
    fig = px.bar(
        prep[prep.Total != 0],
        x=months,
        y="Продавец",
        orientation="h",
        labels={"value": "Продаж"},
        title="Лидеры по продажам",
        template=template_from_url(theme),
    )
    fig.update_layout(legend_title="Months")

    # # Plot chart with applied filter for chosen metric
    # fig = px.line(
    #     df[filt].groupby("Дата", as_index=False)[main_data].agg(agg_m),
    #     x="Дата",
    #     y=main_data,
    #     labels={"value": ""},
    #     template=template_from_url(theme),
    # )
    # # Remove excessive margins
    # fig.update_layout(
    #     margin=dict(
    #         l=0,
    #         r=0,
    #         b=0,
    #     )
    # )

    return fig


# Update top items chart
@callback(
    Output("top-sellers-n-sku-chart", "figure"),
    Input("metric-radio", "value"),
    Input("agg-dd", "value"),
    Input(ThemeChangerAIO.ids.radio("theme"), "value"),
)
@data_access
def update_sellers_n_sku_chart(
    df,
    metric,
    agg_m,
    theme,
):
    # Group by seller and SKU
    prep = df.groupby(["Продавец", "SKU"], as_index=False)["Продажи/день"].sum()
    # Add total by seller
    prep["total"] = prep.groupby("Продавец")["Продажи/день"].transform("sum")
    # Sort for unique
    prep.sort_values(by="total", ascending=False, inplace=True)
    prep.rename(columns={"Продажи/день": "Продаж"}, inplace=True)
    # Add item names
    prep = prep.join(
        df[["SKU", "Название"]]
        .drop_duplicates(subset="SKU", keep="last")
        .set_index("SKU"),
        on="SKU",
        how="left",
    )
    # display(prep[prep['total'].isin(prep["total"].unique()[:10])])
    fig = px.sunburst(
        prep[prep["total"].isin(prep["total"].unique()[:10])],
        path=["Продавец", "SKU"],
        values="Продаж",
        title="Топ 10 продавцов и их пылесосы",
        hover_name="Название",
        template=template_from_url(theme),
    )
    fig.update_traces(textinfo="label+value", insidetextorientation="horizontal")

    return fig

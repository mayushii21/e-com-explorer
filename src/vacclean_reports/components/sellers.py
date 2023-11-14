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
        responsive=True,
        style={"height": "90vh"},
    )


def top_sellers_n_sku_chart():
    return dcc.Graph(
        id="top-sellers-n-sku-chart",
        # config={"modeBarButtonsToRemove": ["select2d", "lasso2d", "zoom"]},
        responsive=True,
        style={"height": "90vh"},
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
    # Handle double metric
    metrics = metric.split()
    # Apply proper formatting
    main_data = (
        metric + "/день" if len(metrics) == 1 else [m + "/день" for m in metrics]
    )

    # Group by seller and month
    prep = df.groupby(["Продавец", pd.Grouper(key="Дата", freq="M")], as_index=False)[
        main_data
    ].agg(agg_m)
    # Pivot months to columns
    prep = prep.pivot(index="Продавец", columns="Дата", values=main_data)
    # Set month names
    months = ["Aug.", "Sept.", "Oct."]
    prep.columns = months
    # Calculate totals and sort
    prep["Total"] = prep.agg(agg_m, axis=1)
    prep.sort_values(by="Total", inplace=True)
    prep.reset_index(inplace=True)
    # Plot
    fig = px.bar(
        prep.tail(40),
        x=months,
        y="Продавец",
        orientation="h",
        labels={"value": metric, "Продавец": ""},
        # title="Топ продавцы",
        template=template_from_url(theme),
    )
    fig.update_layout(
        legend_title="Months",
        margin=dict(
            l=0,
            r=0,
            t=50,
            b=10,
        ),
    )

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
    # Handle double metric
    metrics = metric.split()
    # Apply proper formatting
    main_data = (
        metric + "/день" if len(metrics) == 1 else [m + "/день" for m in metrics]
    )

    # Group by seller and SKU
    prep = df.groupby(["Продавец", "SKU"], as_index=False)[main_data].agg(agg_m)
    # Add total by seller
    prep["total"] = prep.groupby("Продавец")[main_data].transform(agg_m)
    # Sort for unique
    prep.sort_values(by="total", ascending=False, inplace=True)
    prep.rename(columns={main_data: metric}, inplace=True)
    # Add item names
    prep = prep.join(
        df[["SKU", "Название"]]
        .drop_duplicates(subset="SKU", keep="last")
        .set_index("SKU"),
        on="SKU",
        how="left",
    )
    fig = px.sunburst(
        prep[prep["total"].isin(prep["total"].unique()[:10])],
        path=["Продавец", "SKU"],
        values=metric,
        title="Топ продавцы и их товары",
        hover_name="Название",
        template=template_from_url(theme),
    )
    fig.update_traces(textinfo="label+value", insidetextorientation="horizontal")
    # Remove excessive margins
    fig.update_layout(
        margin=dict(
            l=0,
            r=0,
            t=50,
            b=10,
        )
    )

    return fig

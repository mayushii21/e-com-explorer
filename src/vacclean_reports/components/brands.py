import pandas as pd
import plotly.express as px
from dash import dcc
from dash.dependencies import Input, Output
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url

from vacclean_reports.components.decorators import callback, data_access


def top_brands_chart():
    return dcc.Graph(
        id="top-brands-chart",
        responsive=True,
        style={"height": "90vh"},
    )


# Update top brand chart
@callback(
    Output("top-brands-chart", "figure"),
    Input("metric-radio", "value"),
    Input("agg-dd", "value"),
    Input("toggle", "value"),
    Input(ThemeChangerAIO.ids.radio("theme"), "value"),
)
@data_access
def update_brand_chart(
    df,
    metric,
    agg_m,
    toggle,
    theme,
):
    # Handle double metric
    metrics = metric.split()
    # Apply proper formatting
    if len(metrics) == 1:
        main_data = metric + "/день"
    else:
        metric = main_data = "Коэффициент удовлетворения запросов"
        # Use mean for aggregation
        agg_m = "mean" if agg_m == "sum" else agg_m

    # Set barmode
    mode = "group" if toggle else "stack" if agg_m == "sum" else "overlay"

    # Group by brand and month
    prep = df.groupby(["Бренд", pd.Grouper(key="Дата", freq="M")], as_index=False)[
        main_data
    ].agg(agg_m)
    # Pivot months to columns
    prep = prep.pivot(index="Бренд", columns="Дата", values=main_data)
    # Rename months
    months = ["Aug.", "Sept.", "Oct."]
    prep.columns = months
    # Calculate and sort by total
    prep["Total"] = prep.agg(agg_m, axis=1)
    prep.sort_values(by="Total", ascending=False, inplace=True)
    prep.reset_index(inplace=True)
    # Plot
    fig = px.bar(
        prep[prep.Total != 0],
        x="Бренд",
        y=months,
        labels={"value": metric, "x": "SKU"},
        barmode=mode,
        template=template_from_url(theme),
    )
    fig.update_layout(legend_title="Months")

    return fig

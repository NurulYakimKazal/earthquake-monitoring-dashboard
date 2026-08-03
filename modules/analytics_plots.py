import numpy as np
import plotly.graph_objects as go
from utils.empty_graph import empty_chart


def render_frequency_chart(df_trend):

    if df_trend.empty:
        return empty_chart("No frequency data matches the selected filters.")

    df = df_trend.copy()

    df["normalized_time"] = (
        df["datetime"]
        .dt.normalize()
    )

    daily_freq = (
        df.groupby("normalized_time")
        .size()
        .reset_index(name="count")
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=daily_freq["normalized_time"],
            y=daily_freq["count"],
            mode="lines+markers",
            name="Earthquakes",
            line=dict(
                color="#2F5DA8",
                width=2,
            ),
            marker=dict(
                size=6,
                color="#2F5DA8",
                line=dict(
                    color="white",
                    width=2,
                ),
            ),
            hovertemplate=(
                "Date: %{x|%b %d, %Y}<br>"
                "Count: %{y}"
                "<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Date",
        yaxis_title="Count",
        height=450,
        margin=dict(
            t=20,
            l=20,
            r=20,
            b=20,
        ),
    )

    fig.update_xaxes(
        title=dict(standoff=20),
        showgrid=False
    )

    fig.update_yaxes(
        title=dict(standoff=20),
        showgrid=True,
        gridcolor="rgba(0,0,0,0.07)",
        gridwidth=1,
        zeroline=False,
    )

    return fig


def render_rolling_average(df_trend):

    if df_trend.empty:
        return empty_chart("No rolling average data matches the selected filters.")

    df = (
        df_trend
        .sort_values("datetime")
        .set_index("datetime")
        .copy()
    )

    df["rolling_mag"] = (
        df["magnitude"]
        .rolling("7D")
        .mean()
    )

    df = df.reset_index()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["datetime"],
            y=df["rolling_mag"],
            mode="lines",
            name="7-Day Rolling Average",
            line=dict(
                color="#2F5DA8",
                width=2,
            ),
            customdata=df[["magnitude", "place"]],
            hovertemplate=(
                "Date: %{x|%Y-%m-%d %H:%M:%S}<br>"
                "7-Day Avg Magnitude: %{y:.2f}<br>"
                "Event Magnitude: %{customdata[0]:.1f}<br>"
                "Location: %{customdata[1]}"
                "<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Date",
        yaxis_title="Average Magnitude",
        height=450,
        margin=dict(
            t=20,
            l=20,
            r=20,
            b=20,
        ),
    )

    fig.update_xaxes(
        title=dict(standoff=20),
        showgrid=False
    )

    fig.update_yaxes(
        title=dict(standoff=20),
        showgrid=True,
        gridcolor="rgba(0,0,0,0.07)",
        gridwidth=1,
        zeroline=False,
    )

    return fig


def render_magnitude_over_time(df_trend):

    if df_trend.empty:
        return empty_chart("No magnitude data matches the selected filters.")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df_trend["datetime"],
            y=df_trend["magnitude"],
            mode="markers",
            marker=dict(
                size=7,
                color=df_trend["magnitude"],
                colorscale="Viridis",
                opacity=0.9,
                colorbar=dict(
                    title="Magnitude"
                ),
            ),
            customdata=df_trend[["place"]],
            hovertemplate=(
                "Event Time: %{x|%Y-%m-%d %H:%M:%S}<br>"
                "Magnitude: %{y:.1f}<br>"
                "Location: %{customdata[0]}"
                "<extra></extra>"
            ),
            showlegend=False,
        )
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Date",
        yaxis_title="Magnitude",
        height=450,
        margin=dict(
            t=20,
            l=20,
            r=20,
            b=20,
        ),
    )

    fig.update_xaxes(
        title=dict(standoff=20),
        showgrid=False
    )

    fig.update_yaxes(
        title=dict(standoff=20),
        showgrid=True,
        gridcolor="rgba(0,0,0,0.07)",
        gridwidth=1,
        zeroline=False,
    )

    return fig


def render_depth_distribution(df_trend):

    if df_trend.empty:
        return empty_chart("No depth distribution matches the selected filters.")

    values = df_trend["depth"]

    counts, edges = np.histogram(
        values,
        bins=30
    )

    depth_ranges = [
        f"{edges[i]:.1f} - {edges[i + 1]:.1f} km"
        for i in range(len(edges) - 1)
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=(edges[:-1] + edges[1:]) / 2,
            y=counts,
            width=np.diff(edges),
            marker=dict(
                color="#2F5DA8",
                line=dict(
                    color="white",
                    width=1,
                ),
            ),
            customdata=depth_ranges,
            hovertemplate=(
                "Depth Range: %{customdata}<br>"
                "Count: %{y}"
                "<extra></extra>"
            ),
            showlegend=False,
        )
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Depth",
        yaxis_title="Count",
        height=450,
        margin=dict(
            t=20,
            l=20,
            r=20,
            b=20,
        ),
    )

    fig.update_xaxes(
        title=dict(standoff=20),
        showgrid=False
    )

    fig.update_yaxes(
        title=dict(standoff=20),
        showgrid=True,
        gridcolor="rgba(0,0,0,0.07)",
        gridwidth=1,
        zeroline=False,
    )

    return fig


def render_magnitude_distribution(df_trend):

    if df_trend.empty:
        return empty_chart("No magnitude distribution data matches the selected filters.")

    values = df_trend["magnitude"]

    counts, edges = np.histogram(
        values,
        bins=30
    )

    bin_labels = [
        f"{edges[i]:.1f} - {edges[i + 1]:.1f}"
        for i in range(len(edges) - 1)
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=(edges[:-1] + edges[1:]) / 2,
            y=counts,
            width=np.diff(edges),
            marker=dict(
                color="#2F5DA8",
                line=dict(
                    color="white",
                    width=1,
                ),
            ),
            customdata=bin_labels,
            hovertemplate=(
                "Magnitude Range: %{customdata}<br>"
                "Count: %{y}"
                "<extra></extra>"
            ),
            showlegend=False,
        )
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Magnitude",
        yaxis_title="Count",
        height=450,
        margin=dict(
            t=20,
            l=20,
            r=20,
            b=20,
        ),
    )

    fig.update_xaxes(
        title=dict(standoff=20),
        showgrid=False
    )

    fig.update_yaxes(
        title=dict(standoff=20),
        showgrid=True,
        gridcolor="rgba(0,0,0,0.07)",
        gridwidth=1,
        zeroline=False,
    )

    return fig
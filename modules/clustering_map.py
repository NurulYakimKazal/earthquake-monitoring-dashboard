import plotly.graph_objects as go
from utils.empty_graph import empty_chart


def render_ml_cluster_map(dff, show_noise):

    # =========================
    # FILTER NOISE
    # =========================
    if not show_noise:
        dff = dff[dff["cluster"] != -1]

    if dff.empty:
        return empty_chart("No clusters found with current settings. Try adjusting parameters.")

    dff = dff.copy()

    # =========================
    # POINT SIZE
    # =========================
    dff["point_size"] = (
        dff["magnitude"]
        .fillna(0)
        .clip(4, 8)
        * 2
    )

    # =========================
    # COLORS
    # =========================
    palette = [
        "#00DCDC",  # cyan
        "#F59628",  # orange
        "#E63CE6",  # magenta
        "#00DC5A",  # green
        "#F5E63C",  # yellow
        "#00B4E6",  # blue-cyan
        "#F05AA8",  # pink
    ]


    def cluster_color(cluster_id):
        if cluster_id == -1:
            return "#B4B4B4"

        return palette[int(cluster_id) % len(palette)]


    dff["cluster_color"] = dff["cluster"].apply(cluster_color)


    # =========================
    # MAP
    # =========================
    fig = go.Figure()

    fig.add_trace(
        go.Scattermap(
            lat=dff["latitude"],
            lon=dff["longitude"],

            mode="markers",

            marker=dict(
                size=dff["point_size"] + 0.9,
                color="black",
                opacity=0.6
            ),

            hoverinfo="skip",
            showlegend=False
        )
    )


    fig.add_trace(
        go.Scattermap(
            lat=dff["latitude"],
            lon=dff["longitude"],

            mode="markers",

            marker=dict(
                size=dff["point_size"],
                color=dff["cluster_color"],
                opacity=0.6,
            ),

            customdata=dff[
                [
                    "cluster",
                    "magnitude",
                    "depth",
                    "place",
                ]
            ],

            hovertemplate=(
                "<b>Cluster:</b> %{customdata[0]}<br>"
                "<b>Magnitude:</b> %{customdata[1]}<br>"
                "<b>Depth:</b> %{customdata[2]} km<br>"
                "<b>Location:</b> %{customdata[3]}"
                "<extra></extra>"
            ),
            showlegend=False,
        )
    )


    # =========================
    # MAP SETTINGS
    # =========================
    fig.update_layout(
        map=dict(
            style="carto-darkmatter",
            zoom=2,
            center=dict(
                lat=0,
                lon=0,
            ),
        ),
        height=750,
        margin=dict(
            t=0,
            l=0,
            r=0,
            b=0
        ),
        showlegend=False,
        uirevision="earthquake"
    )

    return fig
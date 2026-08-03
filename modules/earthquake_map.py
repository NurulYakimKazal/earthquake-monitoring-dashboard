import plotly.graph_objects as go
from utils.empty_graph import empty_chart


def magnitude_color(magnitude):
    if magnitude < 3:
        return "#3B82F6"
    elif magnitude < 5:
        return "#EAB308"
    elif magnitude < 7:
        return "#EA580C"
    return "#DC2626"


def render_earthquake_map(filtered_dff, unfiltered_dff):

    if filtered_dff.empty:
        return empty_chart("No earthquakes match the selected filters.")

    dff = filtered_dff.copy()

    # =========================
    # LATEST EARTHQUAKE
    # =========================

    latest = (
        unfiltered_dff
        .sort_values("time", ascending=False)
        .head(1)
    )

    # Exclude latest earthquake from regular markers
    if not latest.empty:
        dff = dff[dff["id"] != latest["id"].iloc[0]]

    dff["color"] = dff["magnitude"].apply(
        magnitude_color
    )

    marker_size = (
            dff["magnitude"] * 2
    ).clip(5, 20)


    fig = go.Figure()


    # =========================
    # EARTHQUAKE OUTLINE
    # =========================

    fig.add_trace(
        go.Scattermap(
            lat=dff["latitude"],
            lon=dff["longitude"],

            mode="markers",

            marker=dict(
                size=marker_size + 0.9,
                color="black",
                opacity=0.6
            ),

            hoverinfo="skip",
            showlegend=False
        )
    )


    # =========================
    # EARTHQUAKE MARKERS
    # =========================

    fig.add_trace(
        go.Scattermap(
            lat=dff["latitude"],
            lon=dff["longitude"],

            mode="markers",

            marker=dict(
                size=marker_size,
                color=dff["color"],
                opacity=0.6
            ),

            customdata=dff[
                [
                    "magnitude",
                    "depth",
                    "place",
                    "time_fmt"
                ]
            ],

            hovertemplate=(
                "<b>Magnitude:</b> %{customdata[0]}<br>"
                "<b>Depth:</b> %{customdata[1]} km<br>"
                "<b>Location:</b> %{customdata[2]}<br>"
                "<b>Time:</b> %{customdata[3]}"
                "<extra></extra>"
            ),

            showlegend=False
        )
    )


    # =========================
    # LATEST EARTHQUAKE
    # =========================

    if not latest.empty:

        fig.add_trace(
            go.Scattermap(
                lat=latest["latitude"],
                lon=latest["longitude"],

                mode="markers",

                marker=dict(
                    size=15.6,
                    color="black"
                ),

                hoverinfo="skip",
                showlegend=False
            )
        )


        fig.add_trace(
            go.Scattermap(
                lat=latest["latitude"],
                lon=latest["longitude"],

                mode="markers",

                marker=dict(
                    size=15,
                    color="white"
                ),

                customdata=latest[
                    [
                        "magnitude",
                        "depth",
                        "place",
                        "time_fmt"
                    ]
                ],

                hovertemplate=(
                    "<b>Latest Earthquake</b><br>"
                    "<b>Magnitude:</b> %{customdata[0]}<br>"
                    "<b>Depth:</b> %{customdata[1]} km<br>"
                    "<b>Location:</b> %{customdata[2]}<br>"
                    "<b>Time:</b> %{customdata[3]}"
                    "<extra></extra>"
                ),

                showlegend=False
            )
        )


    # =========================
    # MAP SETTINGS
    # =========================

    fig.update_layout(
        map=dict(
            style="carto-darkmatter",
            zoom=1.96,
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
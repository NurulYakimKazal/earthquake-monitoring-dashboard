import streamlit as st
import pydeck as pdk


def magnitude_color(mag):
    if mag < 3:
        return [0, 200, 0]
    elif mag < 5:
        return [255, 255, 0]
    elif mag < 7:
        return [255, 140, 0]
    return [255, 0, 0]


def render_earthquake_map(dff, view_mode, latest):
    st.subheader("Earthquake Map")

    dff = dff.copy()

    # feature engineering (acceptable in UI layer for Streamlit apps)
    dff["radius"] = (dff["magnitude"] ** 2 * 2000).clip(lower=10000)
    dff["elevation"] = dff["magnitude"] * 10000
    dff["mag_rgb"] = dff["magnitude"].apply(magnitude_color)

    layers = []

    if view_mode == "Heatmap":
        layers.append(
            pdk.Layer(
                "HeatmapLayer",
                data=dff,
                get_position=["longitude", "latitude"],
                get_weight="magnitude",
                radiusPixels=60,
                pickable=True,
            )
        )

    elif view_mode == "Hexagon":
        layers.append(
            pdk.Layer(
                "HexagonLayer",
                data=dff,
                get_position=["longitude", "latitude"],
                radius=50000,
                elevation_scale=50,
                extruded=True,
                pickable=False,
            )
        )

    elif view_mode == "3D Scatter":
        layers.append(
            pdk.Layer(
                "ColumnLayer",
                data=dff,
                get_position=["longitude", "latitude"],
                get_elevation="elevation",
                radius=15000,
                get_fill_color="mag_rgb",
                extruded=True,
                pickable=True,
            )
        )

    else:
        layers.append(
            pdk.Layer(
                "ScatterplotLayer",
                data=dff,
                get_position=["longitude", "latitude"],
                get_fill_color="mag_rgb",
                get_radius="radius",
                opacity=0.75,
                pickable=True,
            )
        )

    if view_mode == "Scatter":
        layers.append(
            pdk.Layer(
                "ScatterplotLayer",
                data=latest,
                get_position=["longitude", "latitude"],
                get_fill_color=[255, 255, 255],
                get_radius=max(
                    latest["magnitude"].iloc[0] * 25000 * 3,
                    10000
                ),
                opacity=1,
                pickable=True,
            )
        )

    view_state = pdk.ViewState(
        latitude=dff["latitude"].mean(),
        longitude=dff["longitude"].mean(),
        zoom=3,
        pitch=60 if view_mode in ["Hexagon", "3D Scatter"] else 0,
    )

    tooltip = {
        "html": """
            <b>Magnitude:</b> {magnitude_fmt}<br/>
            <b>Depth:</b> {depth_fmt} km<br/>
            <b>Location:</b> {place}<br/>
            <b>Time (UTC):</b> {time_fmt}
            """,
        "style": {"backgroundColor": "black", "color": "white"}
    }

    deck = pdk.Deck(
        map_style="dark",
        layers=layers,
        initial_view_state=view_state,
        tooltip=tooltip,
    )

    st.pydeck_chart(deck, width='stretch')
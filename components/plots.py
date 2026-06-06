import altair as alt


def render_frequency_chart(df_trend):
    df_trend["normalized_time"] = df_trend["time"].dt.normalize()
    daily_freq = df_trend.groupby("normalized_time").size().reset_index(name="count")

    line = alt.Chart(daily_freq).mark_line(color="steelblue").encode(
        x=alt.X("normalized_time:T", title="Date", timeUnit="yearmonthdate"),
        y=alt.Y("count:Q", title="Count")
    )

    points = alt.Chart(daily_freq).mark_circle(size=60, color="steelblue").encode(
        x=alt.X(
            "normalized_time:T",
            timeUnit="yearmonthdate",
            axis=alt.Axis(format="%Y/%m/%d", tickCount="week")
        ),
        y="count:Q",
        tooltip=[
            alt.Tooltip("normalized_time:T", timeUnit="yearmonthdate", title="Date", format="%Y-%m-%d"),
            alt.Tooltip("count:Q", title="Count")
        ]
    ).properties(title="Frequency Over Time")

    return line + points


def render_rolling_average(df_trend):
    df_sorted = df_trend.sort_values("datetime").copy()
    df_sorted = df_sorted.set_index("datetime")
    df_sorted["rolling_mag"] = df_sorted["magnitude"].rolling("7D").mean()
    df_sorted = df_sorted.reset_index()

    return alt.Chart(df_sorted).mark_line(
        color="steelblue",
        strokeWidth=2
    ).encode(
        x=alt.X("datetime:T", title="Date", axis=alt.Axis(format="%Y/%m/%d", tickCount="week")),
        y=alt.Y("rolling_mag:Q", title="Average Magnitude"),
        tooltip=[
            alt.Tooltip("datetime:T", title="Date", format="%Y-%m-%d %H:%M:%S"),
            alt.Tooltip("rolling_mag:Q", title="7-Day Rolling Avg Magnitude", format=".2f"),
            alt.Tooltip("magnitude:Q", title="Event Magnitude", format=".1f"),
            alt.Tooltip("place:N", title="Location")
        ]
    ).properties(title="7-Day Rolling Average Magnitude")


def render_magnitude_over_time(df_trend):
    return alt.Chart(df_trend).mark_circle(
        size=40,
        opacity=0.99
    ).encode(
        x=alt.X("time:T", title="Date", axis=alt.Axis(format="%Y/%m/%d", tickCount="week")),
        y=alt.Y("magnitude:Q", title="Magnitude"),
        color=alt.Color(
            "magnitude:Q",
            scale=alt.Scale(scheme="viridis"),
            title="Magnitude"
        ),
        tooltip=[
            alt.Tooltip("time:T", title="Event Time", format="%Y-%m-%d %H:%M:%S"),
            alt.Tooltip("magnitude:Q", title="Magnitude", format=".1f"),
            alt.Tooltip("place:N", title="Location")
        ]
    ).properties(title="Magnitude Over Time")


def render_depth_distribution(df_trend):
    return alt.Chart(df_trend).mark_bar(color="steelblue").encode(
        alt.X("depth:Q", bin=alt.Bin(maxbins=30), title="Depth (km)"),
        alt.Y("count()", title="Frequency")
    ).properties(title="Depth Distribution")


def render_magnitude_distribution(df_trend):
    return alt.Chart(df_trend).mark_bar().encode(
        alt.X("magnitude:Q", bin=alt.Bin(maxbins=30), title="Magnitude"),
        alt.Y("count()", title="Frequency"),
        color=alt.Color(
            "magnitude:Q",
            bin=alt.Bin(maxbins=30),
            scale=alt.Scale(scheme="viridis"),
            title="Magnitude"
        )
    ).properties(title="Magnitude Distribution")
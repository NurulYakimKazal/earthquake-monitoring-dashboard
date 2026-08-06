DEFAULT_KPIS_VALUES = {
    "Total Events": 0,
    "Max Mag": "N/A",
    "Avg Mag": "N/A",
    "Max Depth (Km)": "N/A",
    "Depth < 70 km": "N/A"
}

def prepare_seismic_kpis(df):
    if df.empty:
        return DEFAULT_KPIS_VALUES

    kpi_values = {
        "Total Events": len(df),
        "Max Mag": f"{df['magnitude'].max():.1f}",
        "Avg Mag": f"{df['magnitude'].mean():.1f}",
        "Max Depth (Km)": f"{df['depth'].max():.1f}",
        "Depth < 70 km": f"{(df["depth"] < 70).mean() * 100:.1f}%"
    }

    return kpi_values
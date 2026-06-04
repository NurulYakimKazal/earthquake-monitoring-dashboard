def add_features(df):
    def get_color(mag):
        if mag >= 6:
            return (255, 60, 60)
        elif mag >= 5:
            return (255, 140, 0)
        elif mag >= 3:
            return (255, 220, 80)
        else:
            return (80, 170, 255)

    df = df.copy()
    df["color"] = df["magnitude"].apply(get_color)

    return df
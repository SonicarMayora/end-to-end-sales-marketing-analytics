import pandas as pd
import numpy as np


def generate_marketing_data(days=180, seed=42):

    rng = np.random.default_rng(seed)

    start_date = pd.Timestamp("2025-01-01")
    dates = [start_date + pd.Timedelta(days=i) for i in range(days)]

    data = []

    for date in dates:

        visits = rng.integers(200, 1000)

        # clicks dependen de visitas
        clicks = int(visits * rng.uniform(0.2, 0.5))

        # leads dependen de clicks
        leads = int(clicks * rng.uniform(0.05, 0.15))

        source = rng.choice(["organic", "paid", "social"])

        data.append({
            "date": date,
            "visits": visits,
            "clicks": clicks,
            "leads": leads,
            "source": source
        })

    return pd.DataFrame(data)


if __name__ == "__main__":
    df = generate_marketing_data()
    print(df.head())
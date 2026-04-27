import numpy as np
import pandas as pd


def generate_sales_pipeline_dataset(
    num_leads=2000,
    seed=42,
):
    """
    Generate a synthetic B2B SaaS sales pipeline dataset.

    Returns:
        pandas.DataFrame: Clean dataset with lead, stage, probability,
        deal value, source, industry, rep ownership, and close timing.
    """

    rng = np.random.default_rng(seed)

    # Stage order reflects natural pipeline progression.
    stages = ["lead", "qualified", "proposal", "closed_won", "closed_lost"]
    stage_weights = np.array([0.34, 0.24, 0.18, 0.13, 0.11])

    # Base probabilities rise as a lead moves deeper into the funnel.
    base_stage_probability = {
        "lead": 0.12,
        "qualified": 0.38,
        "proposal": 0.66,
        "closed_won": 1.00,
        "closed_lost": 0.00,
    }

    source_probability_adjustment = {
        "marketing": 0.00,
        "referral": 0.10,
        "outbound": -0.05,
    }

    sales_reps = ["Alex Chen", "Jordan Lee", "Morgan Patel", "Taylor Brooks"]

    # Spread lead creation dates across roughly one year.
    start_date = pd.Timestamp("2025-01-01")
    end_date = pd.Timestamp("2025-12-31")
    date_range_days = (end_date - start_date).days

    created_offsets = rng.integers(0, date_range_days + 1, size=num_leads)
    created_dates = start_date + pd.to_timedelta(created_offsets, unit="D")

    sources = rng.choice(
        ["marketing", "referral", "outbound"],
        size=num_leads,
        p=[0.50, 0.20, 0.30],
    )
    industries = rng.choice(
        ["tech", "retail", "finance"],
        size=num_leads,
        p=[0.45, 0.30, 0.25],
    )
    reps = rng.choice(sales_reps, size=num_leads)
    deal_values = rng.integers(1000, 20001, size=num_leads)

    sampled_stages = rng.choice(stages, size=num_leads, p=stage_weights)

    probabilities = []
    final_stages = []

    for stage, source in zip(sampled_stages, sources):
        # Start from stage-driven conversion likelihood, then boost referrals.
        probability = base_stage_probability[stage] + source_probability_adjustment[source]

        # Add a small amount of noise to avoid identical scores.
        if stage not in {"closed_won", "closed_lost"}:
            probability += rng.normal(0, 0.04)

        probability = float(np.clip(probability, 0.01, 0.99))

        # Closed deals must reflect a final binary outcome.
        if stage in {"closed_won", "closed_lost"}:
            probability = 1.0 if stage == "closed_won" else 0.0
            final_stage = stage
        else:
            # For open pipeline stages, some leads are progressed to a final outcome
            # using their probability as the win chance.
            if rng.random() < 0.22:
                final_stage = "closed_won" if rng.random() < probability else "closed_lost"
                probability = 1.0 if final_stage == "closed_won" else 0.0
            else:
                final_stage = stage

        probabilities.append(round(probability, 2))
        final_stages.append(final_stage)

    # Sales cycle is constrained to 10-90 days per requirement.
    sales_cycle_days = rng.integers(10, 91, size=num_leads)
    close_dates = created_dates + pd.to_timedelta(sales_cycle_days, unit="D")

    df = pd.DataFrame(
        {
            "lead_id": [f"LEAD-{i:05d}" for i in range(1, num_leads + 1)],
            "created_date": pd.to_datetime(created_dates),
            "stage": sampled_stages,
            "final_stage": final_stages,
            "deal_value": deal_values,
            "probability": probabilities,
            "source": sources,
            "industry": industries,
            "sales_rep": reps,
            "close_date": pd.to_datetime(close_dates),
        }
    )

    # Keep output tidy and analysis-friendly.
    df = df.sort_values("created_date").reset_index(drop=True)

    return df


if __name__ == "__main__":
    sales_pipeline_df = generate_sales_pipeline_dataset()
    print(sales_pipeline_df.head())
    print(f"\nRows: {len(sales_pipeline_df)}")
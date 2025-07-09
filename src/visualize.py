import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt

OUTPUT_DIR = r"C:\Users\User\Desktop\gait_analysis_orthosis\data\outputs\visualizations"
CSV_PATH = r"C:\Users\User\Desktop\gait_analysis_orthosis\data\outputs\metrics_csv\gait_metrics.csv"


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_data(csv_path: str) -> pd.DataFrame:
    """Load CSV file with gait metrics."""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found at {csv_path}. Run analyze_gait.py first.")
    return pd.read_csv(csv_path)


def summary_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Return mean and std for each metric per condition."""
    metrics = [col for col in df.columns if col not in ("condicion", "frame")]
    return df.groupby("condicion")[metrics].agg(["mean", "std"])


def plot_time_series(df: pd.DataFrame, metric: str, save: bool = True):
    """Plot the metric over time for both conditions."""
    plt.figure(figsize=(10, 4))
    for cond, data in df.groupby("condicion"):
        plt.plot(data["frame"], data[metric], label=cond)
    plt.title(f"{metric} over time")
    plt.xlabel("Frame")
    plt.ylabel(metric)
    plt.legend()
    plt.tight_layout()

    if save:
        ensure_output_dir()
        path = os.path.join(OUTPUT_DIR, f"{metric}_timeseries.png")
        plt.savefig(path)
        print(f"Saved {path}")
    else:
        plt.show()
    plt.close()


def plot_bar_summary(stats: pd.DataFrame, metric: str, save: bool = True):
    """Bar chart of mean ± std for a given metric."""
    means = stats[metric]["mean"]
    stds = stats[metric]["std"]

    plt.figure(figsize=(6, 4))
    means.plot(kind="bar", yerr=stds, capsize=4)
    plt.title(f"Mean ± SD of {metric}")
    plt.ylabel(metric)
    plt.tight_layout()

    if save:
        ensure_output_dir()
        path = os.path.join(OUTPUT_DIR, f"{metric}_summary.png")
        plt.savefig(path)
        print(f"Saved {path}")
    else:
        plt.show()
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Visualize gait metrics with/without orthosis")
    parser.add_argument("--metric", default="midline_dev", help="Metric to visualize (default: midline_dev)")
    parser.add_argument("--csv", default=CSV_PATH, help="Path to metrics CSV (default: gait_metrics.csv)")
    parser.add_argument("--show", action="store_true", help="Show plots instead of saving to file")
    args = parser.parse_args()

    df = load_data(args.csv)
    stats = summary_stats(df)

    # Time‑series plot
    plot_time_series(df, args.metric, save=not args.show)

    # Summary bar plot
    plot_bar_summary(stats, args.metric, save=not args.show)

    print("Visualization complete.")


if __name__ == "__main__":
    main()
from argparse import ArgumentParser
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


DEFAULT_CSV = Path("results/metrics/gait_metrics.csv")
DEFAULT_OUTPUT_DIR = Path("results/figures")

METRICS = [
    "knee_angle_left",
    "knee_angle_right",
    "midline_deviation",
]


def load_data(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run extract_gait_metrics.py first."
        )

    return pd.read_csv(path)


def save_summary(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    summary = (
        dataframe.groupby("condition")[METRICS]
        .agg(["mean", "std"])
        .round(3)
    )

    summary.columns = [
        f"{metric}_{stat}"
        for metric, stat in summary.columns
    ]

    summary = summary.reset_index()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output_path, index=False)

def plot_boxplot(
    dataframe: pd.DataFrame,
    metric: str,
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    figure, axis = plt.subplots(figsize=(5, 4))

    dataframe.boxplot(
        column=metric,
        by="condition",
        ax=axis,
    )

    axis.set_title(metric.replace("_", " ").title())
    axis.set_xlabel("")
    axis.set_ylabel(metric.replace("_", " ").title())

    figure.suptitle("")
    figure.tight_layout()

    figure.savefig(
        output_dir / f"box_{metric}.png",
        dpi=150,
    )

    plt.close(figure)


def plot_time_series(
    dataframe: pd.DataFrame,
    metric: str,
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    figure, axis = plt.subplots(figsize=(8, 4))

    for condition, group in dataframe.groupby("condition"):
        axis.plot(
            group["frame"],
            group[metric],
            label=condition.replace("_", " "),
        )

    axis.set_xlabel("Frame")
    axis.set_ylabel(metric.replace("_", " ").title())
    axis.legend()

    figure.tight_layout()

    figure.savefig(
        output_dir / f"{metric}_timeseries.png",
        dpi=150,
    )

    plt.close(figure)


def main() -> None:
    parser = ArgumentParser(
        description="Summarize and plot extracted gait metrics."
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=DEFAULT_CSV,
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
    )

    args = parser.parse_args()

    dataframe = load_data(args.csv)

    save_summary(
        dataframe,
        Path("results/metrics/summary_stats.csv"),
    )

    for metric in METRICS:
        plot_boxplot(
            dataframe,
            metric,
            args.output_dir,
        )

        plot_time_series(
            dataframe,
            metric,
            args.output_dir,
        )

    print(f"Saved figures to {args.output_dir}")


if __name__ == "__main__":
    main()
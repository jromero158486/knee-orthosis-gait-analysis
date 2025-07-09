import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import os
from pathlib import Path

CSV_PATH = Path("data/outputs/metrics_csv/gait_metrics.csv")
OUT_DIR = Path("data/outputs/metrics_csv")
PLOTS_DIR = Path("data/outputs/visualizations")

METRICS = ["knee_angle_R", "knee_angle_L", "midline_dev"]


def load_data(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"{path} no existe. Ejecuta analyze_gait.py primero.")
    return pd.read_csv(path)


def summary_stats(df: pd.DataFrame):
    return df.groupby("condicion")[METRICS].agg(["mean", "std"])


def paired_ttest(df: pd.DataFrame, metric: str):
    """Asume mismo nº de cuadros por condición; empareja por índice."""
    con = df[df["condicion"] == "con_ortesis"][metric].reset_index(drop=True)
    sin = df[df["condicion"] == "sin_ortesis"][metric].reset_index(drop=True)
    common_len = min(len(con), len(sin))
    return stats.ttest_rel(con[:common_len], sin[:common_len])


def boxplot_metric(df: pd.DataFrame, metric: str):
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(5,4))
    df.boxplot(column=metric, by="condicion")
    plt.title(f"{metric} by condition")
    plt.suptitle("")
    plt.ylabel(metric)
    path = PLOTS_DIR / f"box_{metric}.png"
    plt.savefig(path)
    plt.close()
    print(f"Saved {path}")


def main():
    df = load_data(CSV_PATH)
    stats_df = summary_stats(df)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stats_df.to_csv(OUT_DIR / "summary_stats.csv")
    print("Resumen estadístico guardado → summary_stats.csv\n")

    # Pruebas t de Student y boxplots
    for metric in METRICS:
        t_res = paired_ttest(df, metric)
        print(f"Paired t-test {metric}: t={t_res.statistic:.3f}, p={t_res.pvalue:.3e}")
        boxplot_metric(df, metric)


if __name__ == "__main__":
    main()
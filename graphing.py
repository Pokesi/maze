import pstats
import os

import matplotlib.pyplot as plt
import pandas as pd
import glob


def plot_time_data(filename: str):
    data = pd.read_csv(filename)
    plt.figure(figsize=(10, 6))
    plt.scatter(data["Maze"], data["Time"], alpha=0.6)
    plt.xlabel("Maze Number")
    plt.ylabel("Time (seconds)")
    plt.title(f"Time per Maze - {filename.split('_')[0]}")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    total_time = data["Time"].sum()
    plt.text(
        0.95,
        0.95,
        f"Total Time: {total_time:.2f} seconds",
        horizontalalignment="right",
        verticalalignment="top",
        transform=plt.gca().transAxes,
        fontsize=10,
        bbox=dict(facecolor="white", alpha=0.8, edgecolor="none"),
    )
    os.makedirs("/graphs", exist_ok=True)
    plt.savefig(f"/graphs/{filename.split('_')[0]}_time_plot.png")
    plt.close()


def plot_cumulative_data(filename: str):
    data = pd.read_csv(filename)
    plt.figure(figsize=(10, 6))
    plt.plot(data["Maze"], data["Time"].cumsum(), marker="o", linestyle="-")
    plt.xlabel("Maze Number")
    plt.ylabel("Cumulative Time (seconds)")
    plt.title(f"Cumulative Time per Maze - {filename.split('_')[0]}")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    os.makedirs("/graphs", exist_ok=True)
    plt.savefig(f"/graphs/{filename.split('_')[0]}_cumulative_plot.png")
    plt.close()


def plot_performance_data(filename: str):
    stats = pstats.Stats(filename)
    stats.sort_stats("cumulative")

    # Extract top 10 functions by cumulative time
    top_functions = stats.stats.items()  # type: ignore
    top_functions = sorted(top_functions, key=lambda x: x[1][3], reverse=True)[:10]

    functions = [f"{func[0]}:{func[1]}" if isinstance(func, tuple) else func for func, _ in top_functions]
    times = [stat[3] for _, stat in top_functions]

    plt.figure(figsize=(12, 6))
    plt.barh(functions, times)
    plt.xlabel("Cumulative Time (seconds)")
    plt.ylabel("Function")
    plt.title(f'Top 10 Time-Consuming Functions - {filename.split("_")[0]}')

    total_operations = sum(stat[0] for _, stat in top_functions)

    # Add total operations text in the top right
    plt.text(
        0.95,
        0.95,
        f"Total Operations: {total_operations:,}",
        horizontalalignment="right",
        verticalalignment="top",
        transform=plt.gca().transAxes,
        fontsize=10,
        bbox=dict(facecolor="white", alpha=0.8, edgecolor="none"),
    )

    plt.tight_layout()
    os.makedirs("/graphs", exist_ok=True)
    plt.savefig(f"/graphs/{filename.split('_')[0]}_performance_plot.png")
    plt.close()


def plot_memory_data(filename: str):
    with open(filename, "r") as f:
        lines = f.readlines()[6:]

    data = [line.split() for line in lines if line.strip()]
    total_memory = float(data[0][1])

    plt.figure(figsize=(10, 6))
    plt.text(
        0.5,
        0.5,
        f"Total Memory Usage: {total_memory:.2f} MiB",
        horizontalalignment="center",
        verticalalignment="center",
        fontsize=20,
    )
    plt.axis("off")
    plt.title(f'Total Memory Usage - {filename.split("_")[0]}')
    plt.tight_layout()
    os.makedirs("/graphs", exist_ok=True)
    plt.savefig(f"/graphs/{filename.split('_')[0]}_memory.png")
    plt.close()


def performance_data(team: str):
    plot_performance_data(f"{team}_cprofile.prof")
    mem_files = sorted(glob.glob("*_mem.prof"))
    if mem_files:
        if team == "A":
            plot_memory_data(mem_files[0])
        else:
            plot_memory_data(mem_files[-1])
    else:
        print(f"No memory profile files found for team {team}")


plot_time_data("A_times.csv")   
plot_cumulative_data("A_times.csv")
plot_time_data("B_times.csv")
plot_cumulative_data("B_times.csv")
performance_data("A")
performance_data("B")

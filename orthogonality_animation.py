"""Animate how random directions become nearly orthogonal in high dimensions."""

from __future__ import annotations

import argparse
from typing import Sequence

import matplotlib
import numpy as np
from matplotlib.animation import FuncAnimation


DEFAULT_DIMENSIONS = (2, 3, 5, 10, 20, 50, 100, 200, 500, 1_000)


def configure_tk_backend():
    """Use Tk so the animation opens in a small desktop window."""
    try:
        import tkinter

        tkinter.Tk().destroy()
        matplotlib.use("TkAgg", force=True)
        import matplotlib.pyplot as plt

        return plt
    except Exception as error:
        raise RuntimeError(
            "This demo needs the system Tk GUI toolkit to open its window. "
            "Install your operating system's Tk package (for example, `tk` on Arch Linux "
            "or `python3-tk` on Debian/Ubuntu), then run the command from a graphical desktop session."
        ) from error


def random_angles(dimensions: int, samples: int, rng: np.random.Generator) -> np.ndarray:
    """Return angles (in degrees) between independent random unit-vector pairs."""
    first = rng.normal(size=(samples, dimensions))
    second = rng.normal(size=(samples, dimensions))
    first /= np.linalg.norm(first, axis=1, keepdims=True)
    second /= np.linalg.norm(second, axis=1, keepdims=True)
    cosine = np.sum(first * second, axis=1).clip(-1.0, 1.0)
    return np.degrees(np.arccos(cosine))


def animate_orthogonality(
    dimensions: Sequence[int] = DEFAULT_DIMENSIONS,
    samples: int = 5_000,
    interval_ms: int = 900,
    seed: int | None = 7,
) -> FuncAnimation:
    """Open an animation of angle distributions as dimensionality increases.

    The returned animation stays live until the Matplotlib window is closed.
    """
    if not dimensions or any(dimension < 2 for dimension in dimensions):
        raise ValueError("dimensions must contain one or more integers of at least 2")
    if samples < 1:
        raise ValueError("samples must be positive")

    rng = np.random.default_rng(seed)
    angle_sets = [random_angles(dimension, samples, rng) for dimension in dimensions]
    mean_offsets = [np.mean(np.abs(angles - 90)) for angles in angle_sets]

    plt = configure_tk_backend()
    figure, (histogram_axis, trend_axis) = plt.subplots(1, 2, figsize=(11, 4.8))
    figure.canvas.manager.set_window_title("Random directions in high dimensions")

    def draw(frame: int) -> None:
        dimension = dimensions[frame]
        angles = angle_sets[frame]

        histogram_axis.clear()
        histogram_axis.hist(angles, bins=np.linspace(0, 180, 61), color="#5b7cfa", alpha=0.88)
        histogram_axis.axvline(90, color="#e55d5d", linestyle="--", linewidth=2, label="90°")
        histogram_axis.set(xlim=(0, 180), ylim=(0, samples * 0.14), xlabel="Angle between two random directions (degrees)", ylabel="Count")
        histogram_axis.set_title(f"Dimension = {dimension:,}")
        histogram_axis.legend(frameon=False)

        trend_axis.clear()
        trend_axis.plot(dimensions, mean_offsets, color="#c5cbd9", linewidth=2)
        trend_axis.scatter(dimensions[: frame + 1], mean_offsets[: frame + 1], color="#5b7cfa", s=42)
        trend_axis.scatter([dimension], [mean_offsets[frame]], color="#e55d5d", s=65, zorder=3)
        trend_axis.set_xscale("log")
        trend_axis.set(xlabel="Dimension (log scale)", ylabel="Mean distance from 90°", title="Angles concentrate around 90°")
        trend_axis.grid(alpha=0.2)
        figure.suptitle("Random directions become almost orthogonal", fontsize=15, fontweight="bold")
        figure.tight_layout()

    animation = FuncAnimation(figure, draw, frames=len(dimensions), interval=interval_ms, repeat=True)
    plt.show()
    return animation


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, default=5_000, help="random pairs per dimension")
    parser.add_argument("--interval", type=int, default=900, help="milliseconds per animation frame")
    parser.add_argument("--seed", type=int, default=7, help="random seed; use a negative value for a fresh run")
    options = parser.parse_args()
    animate_orthogonality(samples=options.samples, interval_ms=options.interval, seed=None if options.seed < 0 else options.seed)


if __name__ == "__main__":
    main()

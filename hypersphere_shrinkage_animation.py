"""Animate how a unit ball's volume retreats into a thin outer shell in high dimensions."""

from __future__ import annotations

import argparse
from typing import Sequence

import matplotlib
from matplotlib.animation import FuncAnimation


DEFAULT_DIMENSIONS = (1, 2, 3, 5, 10, 20, 50, 100, 200, 500, 1_000)


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


def shell_fraction(dimension: int, shell_thickness: float) -> float:
    """Fraction of a unit ball's volume within `shell_thickness` of its surface.

    Volume scales as r**dimension, so the inner ball of radius (1 - shell_thickness)
    holds (1 - shell_thickness)**dimension of the total volume; the rest is shell.
    Using this ratio directly (instead of dividing two gamma-function volumes)
    keeps the computation stable at high dimension, where the volumes themselves
    underflow toward zero.
    """
    return 1.0 - (1.0 - shell_thickness) ** dimension


def animate_hypersphere_shrinkage(
    dimensions: Sequence[int] = DEFAULT_DIMENSIONS,
    shell_thickness: float = 0.01,
    interval_ms: int = 900,
) -> FuncAnimation:
    """Open an animation of a unit ball's volume concentrating into its outer shell.

    The returned animation stays live until the Matplotlib window is closed.
    """
    if not dimensions or any(dimension < 1 for dimension in dimensions):
        raise ValueError("dimensions must contain one or more integers of at least 1")
    if not 0 < shell_thickness < 1:
        raise ValueError("shell_thickness must be between 0 and 1")

    fractions = [shell_fraction(dimension, shell_thickness) for dimension in dimensions]

    plt = configure_tk_backend()
    figure, (bar_axis, trend_axis) = plt.subplots(1, 2, figsize=(11, 4.8))
    figure.canvas.manager.set_window_title("The shrinking hypersphere")

    def draw(frame: int) -> None:
        dimension = dimensions[frame]
        fraction = fractions[frame]

        bar_axis.clear()
        bar_axis.barh([0], [fraction], color="#e55d5d", label="shell")
        bar_axis.barh([0], [1 - fraction], left=[fraction], color="#5b7cfa", label="core")
        bar_axis.set(xlim=(0, 1), yticks=[], xlabel="Share of the unit ball's volume")
        bar_axis.set_title(f"Dimension = {dimension:,}   ·   outer {shell_thickness:.0%} of the radius")
        bar_axis.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=2)

        trend_axis.clear()
        trend_axis.plot(dimensions, fractions, color="#c5cbd9", linewidth=2)
        trend_axis.scatter(dimensions[: frame + 1], fractions[: frame + 1], color="#5b7cfa", s=42)
        trend_axis.scatter([dimension], [fraction], color="#e55d5d", s=65, zorder=3)
        trend_axis.set_xscale("log")
        trend_axis.set(
            xlabel="Dimension (log scale)",
            ylabel="Fraction of volume in the shell",
            ylim=(0, 1.02),
            title="Almost all the volume is shell",
        )
        trend_axis.grid(alpha=0.2)
        figure.suptitle("A ball's volume retreats to a thin outer shell", fontsize=15, fontweight="bold")
        figure.tight_layout(rect=(0, 0.08, 1, 1))

    animation = FuncAnimation(figure, draw, frames=len(dimensions), interval=interval_ms, repeat=True)
    plt.show()
    return animation


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--thickness", type=float, default=0.01, help="shell thickness as a fraction of the radius")
    parser.add_argument("--interval", type=int, default=900, help="milliseconds per animation frame")
    options = parser.parse_args()
    animate_hypersphere_shrinkage(shell_thickness=options.thickness, interval_ms=options.interval)


if __name__ == "__main__":
    main()

# Curse of dimensionality

Small, reproducible demonstrations of high-dimensional geometry effects that
make nearest-neighbor search, similarity scoring, and density estimation
behave unintuitively as dimensionality grows.

## Demos

### `orthogonality_animation.py` — random directions become orthogonal

Two independent random directions are increasingly likely to form an angle
close to 90° as the number of dimensions grows. The program samples pairs of
vectors from a standard normal distribution, normalizes them to the unit
sphere, and measures the angle between every pair. The animation shows both
the changing angle distribution and the shrinking average distance from 90°.

```bash
python orthogonality_animation.py
python orthogonality_animation.py --samples 10000 --interval 600
```

For two independent random unit vectors $a, b \in \mathbb{R}^n$,

$$
\cos(\theta) = a \cdot b, \qquad \mathbb{E}[a \cdot b] = 0, \qquad \mathrm{Var}(a \cdot b) = \frac{1}{n}.
$$

The dot product concentrates near zero as $n$ grows, so the angle
concentrates near 90°.

### `hypersphere_shrinkage_animation.py` — a ball's volume retreats to its shell

A unit ball in $\mathbb{R}^n$ loses almost all of its volume to a thin shell
just inside its surface as $n$ grows. The animation shows, for each
dimension, how a fixed-thickness outer shell holds a fraction of the total
volume that races toward 1.

```bash
python hypersphere_shrinkage_animation.py
python hypersphere_shrinkage_animation.py --thickness 0.05 --interval 600
```

Volume scales as $r^n$, so an inner ball of radius $1 - \varepsilon$ holds a
fraction

$$
\left(\frac{1-\varepsilon}{1}\right)^n = (1-\varepsilon)^n
$$

of the total volume. The complementary shell therefore holds

$$
f(n) = 1 - (1-\varepsilon)^n,
$$

which converges to 1 for any fixed $\varepsilon > 0$ as $n \to \infty$. The
script uses this closed form rather than dividing two gamma-function ball
volumes, which underflow toward zero and lose precision at high dimension.

## Run it

### System dependency

Both animations open a Tk window, so install Tk through your operating
system first. It is intentionally a system dependency rather than a large
Python GUI package:

```bash
# Arch Linux
sudo pacman -S tk

# Debian/Ubuntu
sudo apt install python3-tk
```

Run from a graphical desktop session. For an SSH session, use X11
forwarding (for example, `ssh -X host`).

```bash
git clone https://github.com/thestubbornbat/curse-of-dimensionality.git
cd curse-of-dimensionality
python -m pip install -r requirements.txt
python orthogonality_animation.py
python hypersphere_shrinkage_animation.py
```

## Use from Python

```python
from orthogonality_animation import animate_orthogonality
from hypersphere_shrinkage_animation import animate_hypersphere_shrinkage

animate_orthogonality(dimensions=[2, 10, 100, 1_000], samples=10_000)
animate_hypersphere_shrinkage(dimensions=[1, 10, 100, 1_000], shell_thickness=0.01)
```

## License

[MIT](LICENSE)

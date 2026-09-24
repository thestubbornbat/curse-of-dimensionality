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

# macOS (Homebrew) — see the macOS caveat below before running this
brew install python-tk@3.12
```

Run from a graphical desktop session. For an SSH session, use X11
forwarding (for example, `ssh -X host`).

#### macOS: crash on startup ("Trace/BPT trap: 5")

If the window crashes the instant it tries to open, with a traceback ending
in `_tkinter_tkapp_mainloop` / `showRootWindow` and a `SIGTRAP`, you've hit a
bug in Tcl/Tk 9.0's macOS (Aqua/Cocoa) window backend, not a bug in either
script — `orthogonality_animation.py` crashes the same way. As of writing,
Homebrew's `tcl-tk` formula defaults to 9.0, which is new enough that this
window-showing path is still broken on recent macOS. Tcl/Tk 8.6 does not
have this bug.

**`brew reinstall python-tk@3.12 --build-from-source` does not fix this**,
even after `brew link --force tcl-tk@8` — Homebrew's `python-tk@3.12`
formula hard-depends on the `tcl-tk` formula object (always 9.0 today),
independent of whatever `tcl-tk` version you have linked.

To actually get an 8.6-linked `_tkinter`, build one by hand against
`tcl-tk@8` and drop it in front of the broken one on `sys.path`:

```bash
brew install tcl-tk@8

# Get the matching CPython source (adjust the version to match `python3 --version`)
curl -O https://www.python.org/ftp/python/3.12.14/Python-3.12.14.tgz
tar xzf Python-3.12.14.tgz Python-3.12.14/Modules/_tkinter.c \
	Python-3.12.14/Modules/tkappinit.c Python-3.12.14/Modules/tkinter.h \
	Python-3.12.14/Modules/clinic/_tkinter.c.h
cd Python-3.12.14/Modules

cat > setup.py <<'PY'
from setuptools import setup, Extension
setup(name="tkinter", version="0", ext_modules=[Extension(
    "_tkinter", ["_tkinter.c", "tkappinit.c"],
    define_macros=[("WITH_APPINIT", 1), ("TCL_WITH_EXTERNAL_TOMMATH", 1)],
    include_dirs=["/opt/homebrew/opt/tcl-tk@8/include/tcl-tk"],
    libraries=["tcl8.6", "tk8.6"],
    library_dirs=["/opt/homebrew/opt/tcl-tk@8/lib"],
)])
PY

python3 -m pip install --target=/tmp/tkfix --no-build-isolation .
cp /tmp/tkfix/_tkinter.cpython-312-darwin.so "$(python3 -c 'import site; print(site.getsitepackages()[0])')"
python3 -c "import tkinter; print(tkinter.TclVersion)"  # should print 8.6
```

This overrides `_tkinter` for whichever Python picked it up (a venv's
`site-packages`, if run inside one). Repeat inside each venv, or apply it
once to `python-tk@3.12`'s own `libexec/_tkinter.cpython-312-darwin.so` so
every venv built from that interpreter picks it up automatically. Adjust
the CPython version/include path to match your `python3 --version`.

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

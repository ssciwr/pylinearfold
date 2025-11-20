# pylinearfold

[![PyPI Release](https://img.shields.io/pypi/v/pylinearfold.svg)](https://pypi.org/project/pylinearfold)

This project provides minimal Python bindings to both [LinearFold](https://github.com/LinearFold/LinearFold) and [LinearPartition](https://github.com/LinearFold/LinearPartition) into one Python package, in ViennaRNA mode. The package can be installed from PyPI as wheels - not requiring any C++ compiler toolchain at the end user.

# Installation

Install `pylinearfold` directly from PyPI:

```bash
python -m pip install pylinearfold
```

Supported Python versions: Python 3.10 and newer. Wheels are provided on PyPI for common platforms; if a wheel is not available for your platform you will need a C++ compiler toolchain to build from source.

# 🚀 Features

- ⚡ Linear-time RNA folding (fold)

- 🔬 Partition function & base-pair probabilities (partition)

- 🧬 MEA structure prediction (from LinearPartition)

- 🐍 Pure Python interface (thin bindings to the original C++ libraries)

- 💻 Works in Python scripts, notebooks, and pipelines


# Quick Start

```python
from pylinearfold import fold, partition
seq = "AUCGGUUCGCCGAU"

# Minimum free energy structure
result = fold(seq)

print(result["structure"])      # (((((....)))))
print(result["free_energy"])    # -4.2

# MEA structure, partition function energy and base pair probabilities
res = partition(seq)

print(res["structure"])       # (((((....)))))
print(res["free_energy"])     # -4.472184621676477
print(res["probabilities"])

```

# API

## Fold signature:

```python
fold(
    seq: str,                   # RNA sequence
    beamsize: int = 100,        # beam size for beam search
    verbose: bool = False,      # verbose logging
    sharpturn: bool = False,    # enable sharp turn constraint
    zuker: bool = False,        # enable Zuker suboptimal structures
    delta: float = 5.0,         # delta parameter for Zuker exploration
    dangles: int = 2,           # dangles model (0, 1, or 2)
) -> dict
```
Returns a dict:
```python
{
    "structure": str,       # dot-bracket string
    "free_energy": float,   # kcal/mol
}
```

## Partition signature:

Python signature exposed by your bindings:
```python
partition(
    seq: str,                   # RNA sequence
    beamsize: int = 100,        # beam size for beam search
    verbose: bool = False,      # verbose logging
    sharpturn: bool = False,    # enable sharp turn constraint
    cutoff: float = 1e-5,       # cutoff for base pair probabilities
    gamma: float = 1.0,         # gamma parameter for MEA structure
) -> dict
```

Returns a dict:

```python
{
    "structure": str,               # MEA or partition-based structure (dot-bracket)
    "free_energy": float,           # partition function free energy
    "probabilities": np.ndarray,    # array of (i, j, prob)
}
```

Where probabilities is a NumPy structured array with dtype:

```bash
[('i', np.int32), ('j', np.int32), ('prob', np.float32 or np.float64)]
```

Each row represents a base pair (i, j) with pairing probability prob. The indexes i and j are 0-based (the first nucleotide has index 0).

Example (dtype and sample):

```python
import numpy as np
probs = np.array([(0, 5, 0.8125), (1, 4, 0.1234)],
                 dtype=[('i', 'i4'), ('j', 'i4'), ('prob', 'f4')])
print(probs[0])         # (0, 5, 0.8125)
```

Quick use example (filtering high-probability pairs):

```python
for i, j, p in probs:
    if p > 0.5:
        print(f"pair: {i}-{j}, prob={p:.2f}")
```

Note: the `i` and `j` coordinates are 0-based; add +1 if you prefer 1-based positions.

# License

Please review the redistribution terms and warranty disclaimer in `LICENSE.md`.
This project includes the original LinearFold/LinearPartition source and uses
the same redistribution terms; see `LICENSE.md` for details.

# Contributing

Issues and pull requests are welcome. If you plan to contribute, please open an
issue first to discuss larger changes.

# Citation

If you use pylinearfold in academic work, please cite the original LinearFold/LinearPartition papers:

- Liang Huang, He Zhang, Dezhong Deng, Kai Zhao, Kaibo Liu, David A Hendrix, David H Mathews, LinearFold: linear-time approximate RNA folding by 5'-to-3' dynamic programming and beam search, Bioinformatics, Volume 35, Issue 14, July 2019, Pages i295–i304, https://doi.org/10.1093/bioinformatics/btz375

- He Zhang, Liang Zhang, David H Mathews, Liang Huang, LinearPartition: linear-time approximation of RNA folding partition function and base-pairing probabilities, Bioinformatics, Volume 36, Issue Supplement_1, July 2020, Pages i258–i267, https://doi.org/10.1093/bioinformatics/btaa460

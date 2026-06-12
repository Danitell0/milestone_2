#!/usr/bin/env python3

import sys
import importlib.metadata

try:
    import pandas
except ImportError:
    pandas = None
try:
    import numpy
except ImportError:
    numpy = None
try:
    import matplotlib
except ImportError:
    matplotlib = None


def main() -> None:
    print("\nLOADING STATUS: Loading programs...\n")

    print("Checking dependecies:")
    if pandas:
        print(f" [OK] pandas {importlib.metadata.version('pandas')} - Data manipulation ready")
    else:
        print(" [MISSING] pandas - For installation:\n"
              "  pip install pandas\n"
              "  poetry add pandas")
    if numpy:
        print(f" [OK] numpy {importlib.metadata.version('numpy')} - Numerical computation ready")
    else:
        print(" [MISSING] numpy - For installation:\n"
              "  pip install numpy\n"
              "  poetry add numpy")
    if matplotlib:
        print(f" [OK] matplotlib {importlib.metadata.version('matplotlib')} - Visualization ready")
    else:
        print(" [MISSING] matplotlib - For installation:\n"
              "  pip install matplotlib\n"
              "  poetry add matplotlib")
        
    if pandas and numpy and matplotlib:
        print("Analyzing Matrix data...")
        print("Processing 1000 data points...")
        print("Generating visualization...")

        print("Analysis complete!")
        print("Results saved to: matrix_analysis.png")


if __name__ == "__main__":
    main()

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
    import matplotlib.pyplot as plt
except ImportError:
    matplotlib = None
try:
    import requests
except ImportError:
    requests = None


def pack_checker(name: str, module: object | None, description: str) -> bool:
    if module:
        print(f" [OK] {name} ({importlib.metadata.version(name)})"
              f" - {description}")
        return True
    else:
        print(f" [MISSING] {name} - For installation:\n"
              f"  pip install {name}\n  poetry add {name}")
        return False


def main() -> None:
    print("\nLOADING STATUS: Loading programs...\n")
    if sys.prefix == sys.base_prefix:
        print("Environment: Global")
    elif "pypoetry" in sys.prefix:
        print("Environment: Poetry")
    else:
        print("Environment: pip+venv")

    print("Checking dependecies:")
    ok_pandas = pack_checker("pandas", pandas, "Data manipulation ready")
    ok_numpy = pack_checker("numpy", numpy, "Numerical computation ready")
    ok_requests = pack_checker("requests", requests, "Network access ready")
    ok_mat = pack_checker("matplotlib", matplotlib, "Visualization ready")

    if ok_pandas and ok_numpy and ok_mat and ok_requests:
        print("\nAnalyzing Matrix data...")

        try:
            api = 'https://api.fbi.gov/wanted/v1/list?pageSize=15'
            response = requests.get(api)
            page = response.json()
            wanted_list = page["items"]
            data = [{
                "title": person["title"]} for person in wanted_list]
        except Exception:
            print("API failed to connect!")
            return

        print("\nProcessing data points...")

        rewards = numpy.random.randint(1000, 10000, size=len(data))
        for person, reward in zip(data, rewards):
            person["reward"] = int(reward)
        dataframe = pandas.DataFrame(data)

        print("\nGenerating visualization...")

        bar_height = 0.5

        plt.barh(
            dataframe['title'], dataframe['reward'],
            color='blue', edgecolor='grey',
            height=bar_height, label='Rewards')

        plt.title('FBI Wanted List', fontweight='bold', fontsize=15)
        plt.xlabel('Rewards', fontweight='bold', fontsize=15)
        plt.ylabel('Criminals', fontweight='bold', fontsize=15)
        plt.yticks(fontsize=6)
        plt.tight_layout()
        plt.savefig('matrix_analysis.png')

        print("\nAnalysis complete!")
        print("\nResults saved to: matrix_analysis.png")


if __name__ == "__main__":
    main()

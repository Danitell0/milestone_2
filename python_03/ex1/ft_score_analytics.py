#!/usr/bin/env python3

import sys

if __name__ == "__main__":
    print("=== Fighter Stats Arena ===")
    combo = []
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            try:
                combo.append(int(arg))
            except ValueError:
                print(f"Invalid parameter: '{arg}'")
    if len(combo) == 0:
        print("No damage provided. Usage: python3 "
              "ft_score_analytics.py <hit1> <hit2> ...")
    else:
        print(f"Damage hit: {combo}")
        print(f"Total hits: {len(combo)}")
        print(f"Total damage dealt: {sum(combo)}")
        print(f"Average power: {(sum(combo) / len(combo)):.1f}")
        print(f"Highest hit: {max(combo)}")
        print(f"Lowest hit: {min(combo)}")
        print(f"Combo range: {max(combo) - min(combo)}")

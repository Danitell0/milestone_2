#!/usr/bin/env python3

import sys
import os


def main() -> None:
    print("\nMATRIX STATUS: You're still plugged in\n")

    print(f"Current Python: {sys.executable}")
    print("Virtual Enviroment: ", end="")
    if not os.environ.get('VIRTUAL_ENV'):
        print("None detected")
    else:
        print(os.environ['PATH'])
    print()

if __name__ == "__main__":
    main()

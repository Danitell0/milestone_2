#!/usr/bin/env python3

import sys
import os
import site


def main() -> None:
    venv_path = os.environ.get('VIRTUAL_ENV')

    print("\nMATRIX STATUS: ", end="")
    if not venv_path:
        print("You're still plugged in\n")
    else:
        print("Welcome to the construct\n")

    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: ", end="")

    if not venv_path:
        print("None detected\n")
        print("WARNING: You're in the global environment!\n"
              "The machines can see everything you install.\n"
              "\nTo enter the construct, run:\n"
              "python -m venv matrix_env\n"
              "source matrix_env/bin/activate # On Unix\n"
              "matrix_env\\Scripts\\activate  # On Windows\n")
        print("Then run this program again.")
    else:
        print(os.path.basename(venv_path))
        print(f"Environment Path: {venv_path}\n")

        print("SUCCESS: You're in an isolated environment!\n"
              "Safe to install packages without affecting\n"
              "the global system.\n")
        print("Package installation path:")
        site_p = [
            p for p in site.getsitepackages()
            if venv_path in p and "site-packages" in p
            ]
        print(site_p[0])


if __name__ == "__main__":
    main()

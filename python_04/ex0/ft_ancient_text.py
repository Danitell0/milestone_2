#!/usr/bin/env python3

import sys
import typing


def main():
    if len(sys.argv) == 1:
        print(f"Usage: {sys.argv[0]} <file>\n")
    else:
        print("=== Cyber Archives Recovery ===")
        try:
            print(f"Accessing file '{sys.argv[1]}'...")
            content: typing.IO = open(sys.argv[1])
            print("---\n")
            print(content.read())
            print("\n---")
            content.close()
            print(f"File '{sys.argv[1]}' closed.")
        except Exception as e:
            print(f"Error opening file '{sys.argv[1]}': {e}")


if __name__ == "__main__":
    main()

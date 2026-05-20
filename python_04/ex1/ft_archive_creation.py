#!/usr/bin/env python3

import sys
import typing


def main() -> None:
    if len(sys.argv) == 1:
        print(f"Usage: {sys.argv[0]} <file>\n")
    else:
        print("=== Cyber Archives Recovery ===")
        try:
            print(f"Accessing file '{sys.argv[1]}'...")

            content: typing.IO = open(sys.argv[1])
            print("---\n")
            text = content.read()
            print(text)
            print("\n---")
            content.close()
            print(f"File '{sys.argv[1]}' closed.\n")

            print("Transform data:")
            print("---\n")
            fragments = text.split("\n")
            new_content_str = ""
            for line in fragments:
                if line:
                    new_content_str += line + "#"
            print(new_content_str)
            print("---")

            new_file = str(input("Enter a new file name (or empty): "))
            if new_file:
                print(f"Saving data to '{new_file}'...")
                new_content: typing.IO = open(new_file, "w")
                new_content.write("#".join(new_content_str))
            else:
                    print("Not saving data.")

        except Exception as e:
            print(f"Error opening file '{sys.argv[1]}': {e}")


if __name__ == "__main__":
    main()

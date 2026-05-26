#!/usr/bin/env python3

import sys
import typing


def main() -> None:
    if len(sys.argv) == 1:
        print(f"Usage: {sys.argv[0]} <file>\n")
    else:
        print("=== Cyber Archives Recovery & Preservation ===")
        try:
            print(f"Accessing file '{sys.argv[1]}'...")

            content: typing.IO[str] = open(sys.argv[1])
            print("---\n")
            text = content.read()
            print(text)
            print("\n---")
            content.close()
            print(f"File '{sys.argv[1]}' closed.\n")

            print("Transform data:")
            print("---\n")
            fragments = text.split("\n")
            lines_w_hash = [line + '#' for line in fragments if line]
            new_content_str = '\n'.join(lines_w_hash)
            print(new_content_str)
            print("\n---")

            sys.stdout.write("Enter a new file name (or empty): ")
            sys.stdout.flush()
            new_file = sys.stdin.readline().strip()
            if new_file:
                print(f"Saving data to '{new_file}'...")
                try:
                    new_content: typing.IO[str] = open(new_file, "w")
                    new_content.write(new_content_str)
                    print(f"Data saved in file '{new_file}'.")
                    new_content.close()
                except Exception as e:
                    print(f"[STDERR] Error saving data in "
                          f"{new_file}: {e}", file=sys.stderr)
            else:
                print("Not saving data.")

        except Exception as e:
            print(f"[STDERR] Error opening file "
                  f"'{sys.argv[1]}': {e}", file=sys.stderr)


if __name__ == "__main__":
    main()

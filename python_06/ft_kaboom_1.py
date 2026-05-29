#!/usr/bin/env python3


def main() -> None:
    print("=== Kaboom 1 ===\n"
          "Access to alchemy/grimoire/dark_spellbook.py directly")
    print("Test import now - "
          "THIS WILL RAISE AN UNCAUGHT EXCEPTION")
    import alchemy.grimoire.dark_spellbook  # noqa: F401


if __name__ == "__main__":
    main()

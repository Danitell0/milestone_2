#!/usr/bin/env python3

import alchemy.grimoire


def main() -> None:
    print("=== Kaboom 0 ===\n"
          "Using grimoire module directly")
    spell = "Fantasy"
    ingr_list = "Eart, wind and fire"
    res = alchemy.grimoire.light_spell_record(spell, ingr_list)
    print(f"Testing record light spell: {res}\n")


if __name__ == "__main__":
    main()

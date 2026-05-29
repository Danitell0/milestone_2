#/!usr/bin/env python3

import alchemy.grimoire.light_spellbook


def main() -> None:
    print("=== Kaboom 0 ===\n"
          "Using grimoire module directly")
    spell = "Fantasy"
    ingr_list = ["Eart, wind and fire"]
    print(f"Testing record light spell: "
          f"{alchemy.grimoire.light_spellbook.light_spell_record(spell, ingr_list)}")

if __name__ == "__main__":
    main()

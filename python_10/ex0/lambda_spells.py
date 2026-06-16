#!/usr/bin/env python3

from typing import Any


def artifact_sorter(
        artifacts: list[dict[str, object]]) -> list[dict[str, Any]]:
    return sorted(artifacts, key=lambda artifact: artifact['power'],
                  reverse=True)


def power_filter(
        mages: list[dict[str, Any]], min_power: int) -> list[dict[str, Any]]:
    return list(filter(lambda mage: mage['power'] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda spell: f"* {spell} *", spells))


def mage_stats(mages: list[dict[str, Any]]) -> dict[str, Any]:
    powers = list(map(lambda mage: mage['power'], mages))
    return {'max_power': max(powers),
            'min_power': min(powers),
            'avg_power': round((sum(powers) / len(powers)), 2)}


def main() -> None:
    artifacts = [
                 {'name': 'Crystal Orb', 'power': 85},
                 {'name': 'Magic Wand', 'power': 87},
                 {'name': 'Fire Staff', 'power': 92}]
    spells = ['fireball', 'heal', 'shield']
    mages = [{'name': 'Gandalf', 'power': 285},
             {'name': 'Dumbledore', 'power': 235},
             {'name': 'Daniel', 'power': 2},
             {'name': 'Hagrid', 'power': 380}]

    print("\nTesting artifact sorter...")
    sort_art = artifact_sorter(artifacts)
    print(f"{sort_art[0]['name']} ({sort_art[0]['power']} power)"
          f" comes before "
          f"{sort_art[-1]['name']} ({sort_art[-1]['power']} power)")

    print("\nTesting spell transformer...")
    spell_star = spell_transformer(spells)
    print(*spell_star)

    print("\nTesting mage stats")
    print(mage_stats(mages))


if __name__ == "__main__":
    main()

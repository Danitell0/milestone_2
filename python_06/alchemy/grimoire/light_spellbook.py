#!/usr/bin/env python3

import grimoire


def light_spell_allowed_ingredients() -> list[str]:
    return ["earth", "air", "fire", "water"]

def light_spell_record(spell_name: str, ingredients: str) -> str:
    if validate_ingredients(ingredients):
        print(f"Spell recorded: {spell_name} ({ingredients})")
    else:
        print(f"Not enough ingredients allowed to"
              f" record: {spell_name}")

#!/usr/bin/env python3

from .dark_spellbook import dark_spell_allowed_ingredients


def validate_ingredients(ingredients: str) -> str:
    allowed = dark_spell_allowed_ingredients()
    lowcase_ingredients = ingredients.lower()
    ingredient_list = [
        word.strip(", ") for word in lowcase_ingredients.split()
        ]
    if any(word in allowed for word in ingredient_list):
        return ingredients + " - VALID"
    else:
        return ingredients + " - INVALID"

#!/usr/bin/env python3


def validate_ingredients(ingredients: str) -> str:
    from . import light_spellbook
    allowed = light_spellbook.light_spell_allowed_ingredients()
    lowcase_ingredients = ingredients.lower()
    ingredient_list = [word.strip(", ") for word in lowcase_ingredients.split()]
    if any(word in allowed for word in ingredient_list):
        return ingredients + " - VALID"
    else:
        return ingredients + " - INVALID"

#!/usr/bin/env python3


def light_spell_allowed_ingredients() -> list[str]:
    return ["earth", "air", "fire", "water"]


def light_spell_record(spell_name: str, ingredients: str) -> str:
    from . import light_validator
    output = light_validator.validate_ingredients(ingredients)
    if "INVALID" in output:
        return f"Spell rejected: {spell_name} ({output})"
    else:
        return f"Spell recorded: {spell_name} ({output})"

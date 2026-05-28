#!/usr/bin/env python3

def validate_ingredients(ingredients: str) -> str:
    ingredient_list = [word.strip(", " for word in ingredients.split())]
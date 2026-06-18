#!/usr/bin/env python3

from collections.abc import Callable
from functools import wraps
from typing import Any
import time
import random


def spell_timer(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Casting {func.__name__}...")
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Spell completed in {(end - start):.3f} seconds")
        return result
    return wrapper


@spell_timer
def helper_spell(spell: str) -> str:
    # time.sleep(3)
    return f"Casting {spell}!!"


def power_validator(min_power: int) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            power = kwargs.get('power')
            if power is not None and power >= min_power:
                return func(*args, **kwargs)
            else:
                return "Insufficient power for this spell"
        return wrapper
    return decorator


@power_validator(20)
def fireball(power: int, target: str) -> str:
    return f"{target} was hitted by a Fireball and took {power} HP!"


def retry_spell(max_attempts: int) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    print(f"Spell failed, retrying... "
                          f"(attempt {attempt}/{max_attempts})")
            return f"Spell casting failed after {max_attempts} attempts"
        return wrapper
    return decorator


@retry_spell(3)
def helper_risky(target: str) -> str:
    if random.randint(1, 100) < 50:
        raise ValueError("The spell backfired!")
    return f"{target} was hit successfully!"


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        return len(name) >= 3 and name.replace(" ", "").isalpha()

    @power_validator(10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


def main() -> None:
    print("Testing spell timer...")
    print(f" Result: {helper_spell('bibidibobidiboo')}")

    print("\nTesting power validator...")
    print(fireball(power=50, target='Gandalf'))
    print(fireball(power=5, target='Dumbledore'))

    print("\nTesting retrying spell...")
    print(helper_risky('Bob'))

    print("\nTesting MageGuild...")
    lufalufa = MageGuild()
    print(f"'Daniel' True: {lufalufa.validate_mage_name('Daniel')}")
    print(f"'Merlin 42' False: {lufalufa.validate_mage_name('Merlin 42')}")
    print(f"'Harry Potter' True:"
          f" {lufalufa.validate_mage_name('Harry Potter')}\n")

    print(lufalufa.cast_spell('powerbomb', power=25))
    print(lufalufa.cast_spell('cheap shot', power=5))


if __name__ == "__main__":
    main()

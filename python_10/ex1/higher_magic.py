#!/usr/bin/env python3

from collections.abc import Callable


def flipendo_spell(target: str, power: int) -> str:
    return f"Flipendo hitted {target} and took {power} HP"


def cruccio_spell(target: str, power: int) -> str:
    return f"Cruccio hitted {target} and took {power} HP"


def spell_combiner(spell_1: Callable[[str, int], str],
                   spell_2: Callable[[str, int], str]) -> Callable[
                       [str, int], tuple[str, str]]:
    def wrapper(target: str, power: int) -> tuple[str, str]:
        return (spell_1(target, power), spell_2(target, power))
    return wrapper


def power_amplifier(base_spell: Callable[[str, int], str],
                    multiplier: int) -> Callable[[str, int], str]:
    def wrapper(target: str, power: int) -> str:
        return base_spell(target, (power * multiplier))
    return wrapper


def conditional_caster(condition: Callable[[str, int], bool],
                       spell: Callable[[str, int], str]) -> Callable[
                           [str, int], str]:
    def wrapper(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        else:
            return "The spell backfired!"
    return wrapper


def spell_sequence(spells: list[Callable[[str, int], str]]) -> Callable[
                        [str, int], list[str]]:
    def wrapper(target: str, power: int) -> list[str]:
        return [spell(target, power) for spell in spells]
    return wrapper


def condition(_target: str, power: int) -> bool:
    return power >= 10


def main() -> None:
    print("\nTesting spells")
    print(f"Spell 1: {flipendo_spell('Dobby', 35)}\n"
          f"Spell 2: {cruccio_spell('Bellatrix', 67)}\n")

    print("Testing spell combiner")
    combined_spell = spell_combiner(flipendo_spell, cruccio_spell)
    print("Combined spell result: ", end="")
    print(", ".join(combined_spell('Hedwig', 60)))

    print("\nTesting power amplifier...")
    power_10x = power_amplifier(flipendo_spell, 10)
    print(f"Original: {flipendo_spell('Fred', 35)}")
    print(f"Amplified: {power_10x('Fred', 35)}")

    print("\nTesting conditional caster...")
    over_10 = conditional_caster(condition, cruccio_spell)
    print(over_10('Ron', 8))

    print("\nTesting spell sequence...")
    combo = spell_sequence([cruccio_spell, flipendo_spell, power_10x])
    print(", ".join(combo('Umbridge', 50)))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

from collections.abc import Callable


def mage_counter() -> Callable[[], int]:
    counter = 0

    def wrapper() -> int:
        nonlocal counter
        counter += 1
        return counter
    return wrapper


def spell_accumulator(initial_power: int) -> Callable[[int], int]:
    total_power = initial_power

    def wrapper(amount: int) -> int:
        nonlocal total_power
        total_power += amount
        return total_power
    return wrapper


def enchantment_factory(enchantment_type: str) -> Callable[[str], str]:
    def wrapper(item: str) -> str:
        return f"{enchantment_type} {item}"
    return wrapper


def memory_vault() -> dict[str, Callable[..., object]]:
    vault: dict[str, str] = {}

    def store(key: str, value: str) -> None:
        vault[key] = value

    def recall(key: str) -> str:
        if key not in vault:
            return "Memory not found"
        else:
            return vault[key]
    return {'store': store, 'recall': recall}


def main() -> None:
    print("Testing mage counter...")
    counter_a = mage_counter()
    counter_b = mage_counter()
    print(f" counter_a: {counter_a()}\n"
          f" counter_b: {counter_b()}")
    for _ in range(5):
        counter_a()
    print(f" counter_a: {counter_a()}\n"
          f" counter_b: {counter_b()}")

    print("\nTesting spell accumulator...")
    incrementer = spell_accumulator(100)
    print(f"Base 100, add 20: {incrementer(20)}\n"
          f"Base 100, add 30: {incrementer(30)}")

    print("\nTesting enchantment factory...")
    flame_converter = enchantment_factory("Flaming")
    ice_converter = enchantment_factory("Frozen")
    print(flame_converter("Sword"))
    print(ice_converter("Shield"))

    print("\nTesting memory vault...")
    safe = memory_vault()
    safe['store']('secret', '42')
    print(safe['recall']('secret'))
    print(safe['recall']('unknown'))


if __name__ == "__main__":
    main()

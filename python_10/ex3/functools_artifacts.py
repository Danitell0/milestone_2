#!/usr/bin/env python3

from collections.abc import Callable
from typing import Any
import functools
import operator


def helper_spell(power: int, element: str, target: str) -> str:
    return f"{target} was hitted by {element} and took {power} HP."


def spell_reducer(spells: list[int], operation: str) -> int:
    operations: dict[str, Callable[[int, int], int]] = {
        'add': operator.add,
        'multiply': operator.mul,
        'max': max,
        'min': min
    }
    if not spells:
        return 0
    elif operation not in operations:
        raise ValueError(f"Operation '{operation}' is unknown")
    return functools.reduce(operations[operation], spells)


def partial_enchanter(
        base_enchantment: Callable[[int, str, str], str]
        ) -> dict[str, Callable[[str], str]]:
    fire = functools.partial(base_enchantment, 50, 'fire')
    thunder = functools.partial(base_enchantment, 50, 'thunder')
    ice = functools.partial(base_enchantment, 50, 'ice')
    return {'fire': fire, 'thunder': thunder, 'ice': ice}


@functools.lru_cache
def memoized_fibonacci(n: int) -> int:
    if n < 2:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:
    @functools.singledispatch
    def cast(_: Any) -> str:
        return "Unknown spell type"

    @cast.register(int)
    def _(spell: int) -> str:
        return f"{spell} damage!"

    @cast.register(str)
    def _(spell: str) -> str:
        return f"{spell} was casted!"

    @cast.register(list)
    def _(spell: list[Any]) -> str:
        return f"{len(spell)} spells"

    return cast


def main() -> None:
    print("Testing spell reducer...")
    nb_spell = [10, 45, 65, 25, 14, 8]
    print(f" Sum :{spell_reducer(nb_spell, 'add')}")
    print(f" Product: {spell_reducer(nb_spell, 'multiply')}")
    print(f" Max: {spell_reducer(nb_spell, 'max')}")
    print(f" Min: {spell_reducer(nb_spell, 'min')}")

    print("\nTesting partial enchanter...")
    spell_charger = partial_enchanter(helper_spell)
    print(spell_charger['fire']('Dragon'))
    print(spell_charger['thunder']('Merlin'))

    print("\nTesting memoized fibonacci...")
    print(f" Fib(0): {memoized_fibonacci(0)}\n"
          f" Fib(10): {memoized_fibonacci(10)}\n"
          f" Fib(15): {memoized_fibonacci(15)}")
    print(memoized_fibonacci.cache_info())

    print("\nTesting spell dispatcher")
    dispatch = spell_dispatcher()
    print(dispatch(42))
    print(dispatch('Kamehameha'))
    print(dispatch([1, 2, 3]))
    print(dispatch(6.7))


if __name__ == "__main__":
    main()

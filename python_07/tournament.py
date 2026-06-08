#!/usr/bin/env python3

from ex2.strategies import BattleStrategy
from ex1.factories import HealingCreatureFactory, TransformCreatureFactory
from ex0 import FlameFactory, CreatureFactory


def battle() -> None:
    ...


def main() -> None:
    heal_factory = HealingCreatureFactory()
    trans_factory = TransformCreatureFactory()
    flame_factory = FlameFactory()


    print("Tournament 0 (basic)")

    print(" [ (Charmander+Normal), (Healing+Defensive) ]")
    


if __name__ == "__main__":
    main()

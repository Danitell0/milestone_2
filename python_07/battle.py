#!/usr/bin/env python3

from ex0 import FlameFactory, AquaFactory, CreatureFactory


def creature_training(factory: CreatureFactory) -> None:
    print("Testing factory")
    creature = factory.create_base()
    print(creature.describe())
    print(creature.attack())
    creature = factory.create_evolved()
    print(creature.describe())
    print(creature.attack())


def battle_arena(blue_corner: CreatureFactory,
                 red_corner: CreatureFactory) -> None:
    print("Testing battle")
    blue_creature = blue_corner.create_base()
    red_creature = red_corner.create_base()
    print(blue_creature.describe())
    print(" vs.")
    print(red_creature.describe())
    print(" fight!")
    print(blue_creature.attack())
    print(red_creature.attack())


def main() -> None:
    f_factory = FlameFactory()
    creature_training(f_factory)
    print()
    a_factory = AquaFactory()
    creature_training(a_factory)
    print()
    battle_arena(f_factory, a_factory)


if __name__ == "__main__":
    main()

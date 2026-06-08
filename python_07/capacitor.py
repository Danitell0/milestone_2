#!/usr/bin/env python3

from ex1.factories import HealingCreatureFactory, TransformCreatureFactory


def healing_test(factory: HealingCreatureFactory) -> None:
    print("Testing Creature with healing capability")
    print(" base:")
    creature = factory.create_base()
    print(creature.describe())
    print(creature.attack())
    print(creature.heal())
    print(" evolved:")
    creature = factory.create_evolved()
    print(creature.describe())
    print(creature.attack())
    print(creature.heal())


def transform_test(factory: TransformCreatureFactory) -> None:
    print("Testing Creature with transform capability")
    print(" base:")
    creature = factory.create_base()
    print(creature.describe())
    print(creature.attack())
    print(creature.transform())
    print(creature.attack())
    print(creature.revert())
    print(" evolved:")
    creature = factory.create_evolved()
    print(creature.describe())
    print(creature.attack())
    print(creature.transform())
    print(creature.attack())
    print(creature.revert())


def main() -> None:
    h_factory = HealingCreatureFactory()
    healing_test(h_factory)
    print()
    t_factory = TransformCreatureFactory()
    transform_test(t_factory)


if __name__ == "__main__":
    main()

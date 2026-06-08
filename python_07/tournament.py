#!/usr/bin/env python3

from ex2.strategies import BattleStrategy
from ex1.factories import HealingCreatureFactory, TransformCreatureFactory
from ex0 import FlameFactory, CreatureFactory


def tournament_basic(factory: HealingCreatureFactory, flame_f: CreatureFactory) -> None:
    print("*** Tournament ***")
    heal_creature = factory.create_base()
    flame_creature = flame_f.create_base()
    print("XXX opponents involved\n")

    print("* Battle *")
    print(flame_creature.describe(),
        "\n vs.\n",
        heal_creature.describe(),
        "\n now fight!")



def main() -> None:
    heal_factory = HealingCreatureFactory()
    trans_factory = TransformCreatureFactory()
    flame_factory = FlameFactory()


    print("Tournament 0 (basic)")

    print(" [ (Charmander+Normal), (Healing+Defensive) ]")
    tournament_basic(heal_factory, flame_factory)


if __name__ == "__main__":
    main()

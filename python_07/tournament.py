#!/usr/bin/env python3

from ex0.creatures import CreatureFactory
from ex0.factories import FlameFactory, AquaFactory
from ex1.factories import HealingCreatureFactory, TransformCreatureFactory
from ex2.strategies import (BattleStrategy,
                            NormalStrategy,
                            AggressiveStrategy,
                            DefensiveStrategy)


def battle(opponents: list[tuple[CreatureFactory, BattleStrategy]]) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")

    for i in range(len(opponents)):
        for j in range(i + 1, len(opponents)):
            factory_i, strategy_i = opponents[i]
            factory_j, strategy_j = opponents[j]
            creature_i = factory_i.create_base()
            creature_j = factory_j.create_base()

            print("\n* Battle *")
            print(creature_i.describe())
            print(" vs")
            print(creature_j.describe())
            print(" now fight!")
            try:
                strategy_i.act(creature_i)
                strategy_j.act(creature_j)
            except Exception as e:
                print(f"Battle error, aborting tournament: {e}")


def main() -> None:
    print("Tournament 0 (basic)")
    print(" [ (Charmander+Normal), (Healing+Defensive) ]")
    battle([(FlameFactory(), NormalStrategy()),
            (HealingCreatureFactory(), DefensiveStrategy())])

    print("\nTournament 1 (error)")
    print(" [ (Charmander+Aggressive), (Healing+Defensive) ]")
    battle([(FlameFactory(), AggressiveStrategy()),
            (HealingCreatureFactory(), DefensiveStrategy())])

    print("\nTournament 2 (multiple)")
    print(" [ (Squirtle+Normal), (Healing+Defensive), (Transform+Agressive) ]")
    battle([(AquaFactory(), NormalStrategy()),
            (HealingCreatureFactory(), DefensiveStrategy()),
            (TransformCreatureFactory(), AggressiveStrategy())])


if __name__ == "__main__":
    main()

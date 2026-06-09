#!/usr/bin/env python3

import abc
import typing
from ex0.creatures import Creature
from ex1.capabilities import TransformCapability, HealCapability


class BattleStrategy(abc.ABC):
    @abc.abstractmethod
    def act(self, creature: Creature) -> None:
        ...

    @abc.abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        ...


class NormalStrategy(BattleStrategy):
    def act(self, creature: Creature) -> None:
        print(creature.attack())

    def is_valid(self, _: Creature) -> bool:
        return True


class AggressiveStrategy(BattleStrategy):
    def act(self, creature: Creature) -> None:
        if not self.is_valid(creature):
            raise Exception(f"Invalid Creature '{creature.name}'"
                            f" for this aggressive strategy")
        t_creature = typing.cast(TransformCapability, creature)
        print(t_creature.transform())
        print(creature.attack())
        print(t_creature.revert())

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)


class DefensiveStrategy(BattleStrategy):
    def act(self, creature: Creature) -> None:
        if not self.is_valid(creature):
            raise Exception(f"Invalid Creature '{creature.name}'"
                            f" for this defensive strategy")
        h_creature = typing.cast(HealCapability, creature)
        print(creature.attack())
        print(h_creature.heal())

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, HealCapability)

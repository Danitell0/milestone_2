#!/usr/bin/env python3

import abc
from ex0.creatures import Creature


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

    def is_valid(self, creature: Creature) -> bool:
        return True

class AggressiveStrategy(BattleStrategy):
    ...

class DefensiveStrategy(BattleStrategy):
    ...

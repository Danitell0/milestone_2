#!/usr/bin/env python3

import abc


class BattleStrategy(abc.ABC):
    @abc.abstractmethod
    def act(self) -> None:
        ...

    @abc.abstractmethod
    def is_valid(self) -> bool:
        ...


class NormalStrategy(BattleStrategy):
    ...

class AggressiveStrategy(BattleStrategy):
    ...

class DefensiveStrategy(BattleStrategy):
    ...

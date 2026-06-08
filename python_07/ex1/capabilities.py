#!/usr/bin/env python3

import abc
from ex0.creatures import Creature


class HealCapability(abc.ABC):
    @abc.abstractmethod
    def heal(self) -> str:
        ...


class TransformCapability(abc.ABC):
    def __init__(self) -> None:
        self.transformed = False

    @abc.abstractmethod
    def transform(self) -> str:
        ...

    @abc.abstractmethod
    def revert(self) -> str:
        ...


class HealingCreature(Creature, HealCapability):
    ...


class TransformCreature(Creature, TransformCapability):
    ...

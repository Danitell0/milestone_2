#!/usr/bin/env python3

from ex0.creatures import CreatureFactory
from .creatures import (Sproutling, Bloomelle, Togepi, Togetic)
from .capabilities import HealingCreature, TransformCreature


class HealingCreatureFactory(CreatureFactory):
    def create_base(self) -> HealingCreature:
        return Sproutling()

    def create_evolved(self) -> HealingCreature:
        return Bloomelle()


class TransformCreatureFactory(CreatureFactory):
    def create_base(self) -> TransformCreature:
        return Togepi()

    def create_evolved(self) -> TransformCreature:
        return Togetic()

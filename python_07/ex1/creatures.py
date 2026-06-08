#!/usr/bin/env python3

from ex0.creatures import Creature
from .capabilities import (
            TransformCapability,
            HealCapability,
            TransformCreature,
            HealingCreature
)


class Togepi(TransformCreature):
    def __init__(self) -> None:
        Creature.__init__(self, "Togepi", "Fairy")
        TransformCapability.__init__(self)

    def transform(self) -> str:
        self.transformed = True
        return f"{self.name} shifts into its prime form!"

    def revert(self) -> str:
        self.transformed = False
        return f"{self.name} returns to normal."

    def attack(self) -> str:
        if self.transformed:
            return f"{self.name} uses a Boosted Quick Attack!"
        return f"{self.name} uses Quick Attack!"


class Togetic(TransformCreature):
    def __init__(self) -> None:
        Creature.__init__(self, "Togetic", "Fairy/Flying")
        TransformCapability.__init__(self)

    def transform(self) -> str:
        self.transformed = True
        return f"{self.name} morphs into shiny form!"

    def revert(self) -> str:
        self.transformed = False
        return f"{self.name} stabilizes its form."

    def attack(self) -> str:
        if self.transformed:
            return f"{self.name} unleashes a devastating Bite!"
        return f"{self.name} uses Bite!"


class Sproutling(HealingCreature):
    def __init__(self) -> None:
        HealCapability.__init__(self)
        Creature.__init__(self, "Sproutling", "Grass")

    def attack(self) -> str:
        return f"{self.name} uses Vine Whip!"

    def heal(self) -> str:
        return f"{self.name} heals itself for a small amount"


class Bloomelle(HealingCreature):
    def __init__(self) -> None:
        HealCapability.__init__(self)
        Creature.__init__(self, "Bloomelle", "Grass/Dragon")

    def attack(self) -> str:
        return f"{self.name} uses Petal Dance!"

    def heal(self) -> str:
        return f"{self.name} heals itself and others for a large amount"

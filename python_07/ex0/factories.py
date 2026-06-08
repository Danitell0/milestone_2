#!/usr/bin/env python3

from .creatures import (
    Creature,
    CreatureFactory,
    Charmander,
    Charizard,
    Squirtle,
    Blastoise
)


class FlameFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Charmander()

    def create_evolved(self) -> Creature:
        return Charizard()


class AquaFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Squirtle()

    def create_evolved(self) -> Creature:
        return Blastoise()

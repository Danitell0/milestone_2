#!/usr/bin/env python3

import abc


class Creature(abc.ABC):
    def __init__(self, name: str, creature_type: str) -> None:
        self.name = name
        self.creature_type = creature_type

    @abc.abstractmethod
    def attack(self) -> str:
        ...

    def describe(self) -> str:
        return f"{self.name} is a {self.creature_type} type Creature"


class CreatureFactory(abc.ABC):
    @abc.abstractmethod
    def create_base(self) -> Creature:
        ...

    @abc.abstractmethod
    def create_evolved(self) -> Creature:
        ...


class Charmander(Creature):
    def __init__(self) -> None:
        super().__init__("Charmander", "Fire")

    def attack(self) -> str:
        return f"{self.name} uses Ember!"


class Charizard(Creature):
    def __init__(self) -> None:
        super().__init__("Charizard", "Fire/Flying")

    def attack(self) -> str:
        return f"{self.name} uses Flame Wheel!"


class Squirtle(Creature):
    def __init__(self) -> None:
        super().__init__("Squirtle", "Water")

    def attack(self) -> str:
        return f"{self.name} uses Water Gun!"


class Blastoise(Creature):
    def __init__(self) -> None:
        super().__init__("Blastoise", "Water")

    def attack(self) -> str:
        return f"{self.name} uses Hydro Pump!"

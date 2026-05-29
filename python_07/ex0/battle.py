#!/usr/bin/env python3

import typing
import abc


class Creature:
    def __init__(self, name: str, type: str) -> None:
        self.__name = name
        self.__type = type

    @abc.abstractmethod
    def attack(self) -> str:
        ...

    def describe(self) -> str:
        return f"{self.__name} is a {self.__type} type Creature"


class Charmander(Creature):
    def __init__(self, name: str, type: str) -> None:
        super().__init__(name, type)

    def attack(self) -> str:
        return f"{self.name} uses Ember!"

class Cyndaquil(Creature):
    ...

class Squirtle(Creature):
    ...

class Poliwag(Creature):
    ...


def main():
    print("Testing factory")
    charmander = Charmander("Charmander", "Fire")
    print(charmander.describe())
    print(charmander.attack())

if __name__ == "__main__":
    main()

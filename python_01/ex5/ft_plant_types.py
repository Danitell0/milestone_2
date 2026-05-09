#!/usr/bin/env python3

class Plant:
    def __init__(self, name: str, height: float,
                 age: int) -> None:
        self.name = name
        self.set_height(height)
        self.set_age(age)
        self.show()

    def grow(self) -> None:
        self._height += 0.8

    def age(self) -> None:
        self._age += 1

    def show(self) -> None:
        print(f"{self.name}: {round(self._height, 1)}cm, "
              f"{self._age} days old")

    def get_height(self) -> float:
        return self._height

    def set_height(self, value: float) -> None:
        if value < 0:
            print(f"{self.name}: Error, height can't be negative")
            print("Height update rejected")
        else:
            self._height = value

    def get_age(self) -> int:
        return self._age

    def set_age(self, value: int) -> None:
        if value < 0:
            print(f"{self.name}: Error, age can't be negative")
            print("Age update rejected")
        else:
            self._age = value


class Flower(Plant):
    def __init__(self, name: str, height: float, age: int, color: str) -> None:
        self._color = color
        self._bloom = False
        super().__init__(name, height, age)

    def bloom(self) -> None:
        self._bloom = True

    def show(self) -> None:
        super().show()
        print(f"Color: {self._color}")
        if self._bloom:
            print(f"{self.name} is blooming beautifully!")
        else:
            print(f"{self.name} has not bloomed yet")


class Tree(Plant):
    def __init__(self, name: str, height: float, age:
                 int, trunk_diameter: float):
        self._trunk = trunk_diameter
        super().__init__(name, height, age)

    def produce_shade(self) -> None:
        print(f"Tree {self.name} now produce a shade of "
              f"{self._height}cm long and {self._trunk}cm wide.")

    def show(self) -> None:
        super().show()
        print(f"Trunk diameter: {self._trunk}cm")


class Vegetable(Plant):
    def __init__(self, name: str, height: float,
                 age: int, harvest_season: str) -> None:
        self._harvest_season = harvest_season
        self._nutritional_value = 0
        super().__init__(name, height, age)

    def age(self) -> None:
        super().age()
        self._nutritional_value += 1

    def grow(self) -> None:
        super().grow()
        self._height += 1.3

    def show(self) -> None:
        super().show()
        print(f"Harvest season: {self._harvest_season}")
        print(f"Nutritional value: {self._nutritional_value}")


if __name__ == "__main__":
    print("=== Garden Plant Types ===")
    print("=== Flower")
    rose = Flower("Rose", 15.0, 10, "red")
    rose.bloom()
    print()
    rose.show()
    print("\n=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    oak.produce_shade()
    print()
    oak.show()
    print("\n=== Vegetable")
    tomato = Vegetable("Tomato", 5.0, 10, "April")
    print()
    for i in range(20):
        tomato.grow()
        tomato.age()
    tomato.show()

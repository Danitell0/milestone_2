#!/usr/bin/env python3

class Plant:
    class Stats:
        def __init__(self) -> None:
            self._grow_count = 0
            self._age_count = 0
            self._show_count = 0

        def display(self) -> None:
            print(f"Stats: {self._grow_count} grow, "
                  f"{self._age_count} age, {self._show_count} show")

    def __init__(self, name: str, height: float,
                 age: int, grow_rate: float = 0.8) -> None:
        self.name = name
        self._grow_rate = grow_rate
        self._stats = Plant.Stats()
        self.set_height(height)
        self.set_age(age)
        self.show()

    def grow(self) -> None:
        self._height += self._grow_rate
        self._stats._grow_count += 1

    def age(self) -> None:
        self._age += 1
        self._stats._age_count += 1

    def show(self) -> None:
        self._stats._show_count += 1
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

    def show_stats(self) -> None:
        self._stats.display()

    @staticmethod
    def age_check(value: int) -> bool:
        return value > 365

    @classmethod
    def create_anon(cls) -> "Plant":
        unknown = Plant("Unknown plant", 0.0, 0)
        return unknown


def display_stats(plant: Plant) -> None:
    plant.show_stats()


class Flower(Plant):
    def __init__(self, name: str, height: float,
                 age: int, color: str, grow_rate: float = 0.8) -> None:
        self._color = color
        self._bloom = False
        super().__init__(name, height, age, grow_rate)

    def bloom(self) -> None:
        self._bloom = True

    def show(self) -> None:
        super().show()
        print(f"Color: {self._color}")
        if self._bloom:
            print(f"{self.name} is blooming beautifully!")
        else:
            print(f"{self.name} has not bloomed yet")

    def show_stats(self):
        super().show_stats()


class Seed(Flower):
    def __init__(self, name: str, height: float, age: int,
                 color: str, seed_count: int, grow_rate: float = 0.8) -> None:
        self._seed_count = seed_count
        self._show_seeds = 0
        super().__init__(name, height, age, color, grow_rate)

    def bloom(self) -> None:
        super().bloom()
        self._show_seeds = self._seed_count

    def show(self) -> None:
        super().show()
        print(f"Seeds: {self._show_seeds}")


class Tree(Plant):
    def __init__(self, name: str, height: float, age:
                 int, trunk_diameter: float) -> None:
        self._trunk = trunk_diameter
        self._shade_count = 0
        super().__init__(name, height, age)

    def produce_shade(self) -> None:
        self._shade_count += 1
        print(f"Tree {self.name} now produce a shade of "
              f"{self._height}cm long and {self._trunk}cm wide.")

    def show(self) -> None:
        super().show()
        print(f"Trunk diameter: {self._trunk}cm")

    def show_stats(self) -> None:
        super().show_stats()
        print(f"{self._shade_count} shade")


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
    print("=== Garden statistics ===")

    print("=== Check year-old")
    print(f"Is 30 days more than a year? -> {Plant.age_check(30)}")
    print(f"Is 400 days more than a year? -> {Plant.age_check(400)}")

    print("\n=== Flower")
    rose = Flower("Rose", 15.0, 10, "red", 0.8)
    print()
    display_stats(rose)
    rose.age()
    rose.bloom()
    rose.show()
    display_stats(rose)

    print("\n=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    print()
    display_stats(oak)
    print()
    oak.produce_shade()
    print()
    display_stats(oak)

    print("\n=== Seed")
    sunflower = Seed("Sunflower", 80.0, 45, "yellow", 42, 30)
    print()
    sunflower.age()
    sunflower.grow()
    sunflower.bloom()
    sunflower.show()
    print()
    sunflower.show_stats()
    print("\n=== Anonymous")
    anon = Plant.create_anon()
    print()
    display_stats(anon)

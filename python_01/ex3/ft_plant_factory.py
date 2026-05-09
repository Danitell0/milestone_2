#!/usr/bin/env python3

class Plant:
    def __init__(self, name: str, starting_height: float,
                 starting_age: int) -> None:
        print("Created: ", end="")
        self.name = name
        self.starting_height = starting_height
        self.starting_age = starting_age
        self.show()

    def grow(self) -> None:
        self.starting_height += 0.8

    def age(self) -> None:
        self.starting_age += 1

    def show(self) -> None:
        print(f"{self.name}: {round(self.starting_height, 1)}cm, "
              f"{self.starting_age} days old")


if __name__ == "__main__":
    print("=== Plant Factory Output ===")
    rose = Plant("Rose", 25.0, 30)
    oak = Plant("Oak", 200.0, 365)
    cactus = Plant("Cactus", 5.0, 90)
    sunflower = Plant("Sunflower", 80.0, 45)
    fern = Plant("Fern", 15, 120)

#!/usr/bin/env python3

class Plant:
    def __init__(self, name: str, height: float, old: int) -> None:
        self.name = name
        self.height = height
        self.old = old

    def grow(self) -> None:
        self.height += 0.8

    def age(self) -> None:
        self.old += 1

    def show(self) -> None:
        print(f"{self.name}: {round(self.height, 1)}cm, {self.old} days old")


if __name__ == "__main__":
    rose = Plant("Rose", 25.0, 30)
    first_day = rose.height
    print("=== Garden Plant Growth ===")
    rose.show()
    for i in range(1, 8):
        print(f"=== Day {i} ===")
        rose.grow()
        rose.age()
        rose.show()
    print(f"Growth this week: {round(rose.height - first_day, 1)}cm")

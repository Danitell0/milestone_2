#!/usr/bin/env python3

class Plant:
    def __init__(self, name: str, height: float,
                 age: int) -> None:
        print("Plant created: ", end="")
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


if __name__ == "__main__":
    print("=== Garden Security System  ===")
    rose = Plant("Rose", 25.0, 30)
    print()
    rose.set_height(25.0)
    print("Height updated: 25cm")
    rose.set_age(30)
    print("Age updated: 30 days\n")
    rose.set_height(-42)
    rose.set_age(-42)
    print("\nCurrent state: ", end="")
    rose.show()

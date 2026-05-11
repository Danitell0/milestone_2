#!/usr/bin/env python3

class GardenError(Exception):
    def __init__(self, message: str = "Unknown plant error"):
        self.__message = message
        super().__init__(message)


class PlantError(GardenError):
    def __init__(self, message: str = "Unknown plant error"):
        super().__init__(message)


class WaterError(GardenError):
    def __init__(self, message: str = "Unknown plant error"):
        super().__init__(message)


def test_plant_error() -> None:
    try:
        raise PlantError("The tomato plant is wilting!")
    except PlantError as e:
        print(f"Caught PlantError: {e}")


def test_water_error() -> None:
    try:
        raise WaterError("Not enough water in the tank!")
    except WaterError as e:
        print(f"Caught WaterError: {e}")


def test_all_errors() -> None:
    try:
        raise PlantError("The tomato plant is wilting!")
    except GardenError as e:
        print(f"Caught GardenError: {e}")

    try:
        raise WaterError("Not enough water in the tank!")
    except GardenError as e:
        print(f"Caught GardenError: {e}")


if __name__ == "__main__":
    print("=== Custom Garden Errors Demo ===")
    print("\nTesting PlantError...")
    test_plant_error()
    print("\nTesting WaterError...")
    test_water_error()
    print("\nTesting catching all garden errors...")
    test_all_errors()
    print("\nAll custom error types work correctly!")

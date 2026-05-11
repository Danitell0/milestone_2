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

def water_plant(plant_name: str) -> None:


def test_watering_system() -> None:
    print("Opening watering system")
    try:

    except PlantError as e:
        print(f"Caught PlantError: {e}")
    finally:
        print("Closing watering system")

if __name__ == "__main__":
    print("=== Garden Watering System ===")
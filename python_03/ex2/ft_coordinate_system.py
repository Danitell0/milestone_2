#!/usr/bin/env python3

import math


def get_player_pos() -> tuple[float, float, float]:
    while True:
        user_input = input("Enter new coordinates as "
                           "floats 'x,y,z': ").split(",")
        if (len(user_input) != 3):
            print("Invalid syntax")
            continue
        else:
            coordinates = []
            for i in user_input:
                try:
                    coordinates.append(float(i.strip()))
                except ValueError as e:
                    print(f"Error on parameter '{i}': {e}")
            if len(coordinates) != 3:
                continue
            return (coordinates[0], coordinates[1], coordinates[2])


def main() -> None:
    print("=== Game Coordination System ===")
    print("Get a first set of coordinates")
    coordinates_1 = get_player_pos()
    print(f"Got a first tuple: {coordinates_1}")
    print(f"It includes: X={coordinates_1[0]},"
          f" Y={coordinates_1[1]},"
          f" Z={coordinates_1[2]}")
    print(f"Distance to center: {(math.sqrt(coordinates_1[0]**2 +
                                            coordinates_1[1]**2 +
                                            coordinates_1[2]**2)):.5}\n")
    print("Get a second set of coordinates")
    coordinates_2 = get_player_pos()
    position_3d = math.sqrt((coordinates_2[0] - coordinates_1[0])**2 +
                            (coordinates_2[1] - coordinates_1[1])**2 +
                            (coordinates_2[2] - coordinates_1[2])**2)
    print(f"Distance between the 2 sets of coordinates: {position_3d:.5}")


if __name__ == "__main__":
    main()

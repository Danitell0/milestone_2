#!/usr/bin/env python3

import sys


def main() -> None:
    print("=== Inventory Analysis ===")

    if len(sys.argv) > 1:
        inventory: dict[str, int] = {}
        for arg in sys.argv[1:]:
            parts = arg.split(':')
            if len(parts) != 2:
                print(f"Error - invalid parameter '{arg}'")
            else:
                try:
                    quantity = int(parts[1])
                    if parts[0] in inventory:
                        print(f"Redundant item '{parts[0]}' - discarding")
                    else:
                        inventory.update({parts[0]: quantity})
                except ValueError as e:
                    print(f"Quantity error for '{parts[0]}': {e}")

        if inventory:
            print(f"Got inventory: {inventory}")
            inventory_list = list(inventory.keys())
            print(f"Item list: {inventory_list}")
            print(f"Total quantity of the {len(inventory.keys())} "
                  f"items: {sum(inventory.values())}")
            first_key = list(inventory.keys())[0]
            max_value = inventory[first_key]
            min_value = inventory[first_key]
            max_key = first_key
            min_key = first_key

            for key in inventory.keys():
                print(f"Item {key} represents "
                      f"{(inventory[key] / sum(inventory.values())
                          * 100):.1f}%")
                if inventory[key] > max_value:
                    max_value = inventory[key]
                    max_key = key
                elif inventory[key] < min_value:
                    min_value = inventory[key]
                    min_key = key
            print(f"Item most abundant: {max_key} with quantity {max_value}")
            print(f"Item least abundant: {min_key} with quantity {min_value}")

            inventory.update({"magic_item": 1})
            print(f"Updated inventory: {inventory}")


if __name__ == "__main__":
    main()

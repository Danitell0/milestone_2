#!/usr/bin/env python3

import random

achievements = ['Shroooooooms...', 'Im a Super Star!', '1-Up',
                'A-Maze-ing!', 'Going for a Dip', "She's in Another What??",
                'Saved the Girl', 'Saved the Girl Again!', 'Shell Shock',
                'Toasty!', 'Boogie Beans', 'I Know a Shortcut!', 'Sky High']


def gen_player_achievements() -> set:
    user = set(random.sample(achievements, k=random.randint(5, 13)))
    return user


def main() -> None:
    print("=== Achievement Tracker System ===\n")
    mario = gen_player_achievements()
    print(f"Player Mario: {mario}")
    luigi = gen_player_achievements()
    print(f"Player Luigi: {luigi}")
    peach = gen_player_achievements()
    print(f"Player Peach: {peach}")
    yoshi = gen_player_achievements()
    print(f"Player Yoshi: {yoshi}\n")
    print(f"All distinct achievements: {mario | luigi | peach | yoshi}\n")
    print(f"Common achievements: {mario & luigi & peach & yoshi}\n")
    print(f"Only Mario has: {mario.difference(luigi, peach, yoshi)}")
    print(f"Only Luigi has: {luigi.difference(mario, peach, yoshi)}")
    print(f"Only Peach has: {peach.difference(mario, luigi, yoshi)}")
    print(f"Only Yoshi has: {yoshi.difference(mario, luigi, peach)}\n")
    print(f"Mario is missing: {set(achievements) - mario}")
    print(f"Luigi is missing: {set(achievements) - luigi}")
    print(f"Peach is missing: {set(achievements) - peach}")
    print(f"Yoshi is missing: {set(achievements) - yoshi}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import random


player_list = ["Costa", "cancelo", "Fernandes", "Ferreira",
               "jota", "felix", "Dias", "neves", "silva"]


def main() -> None:
    print("=== Game Data Alchemist ===\n")

    print(f"Initial list of players: {player_list}\n")
    capitalized_player_list_only = [player for player in player_list
                                    if player == player.capitalize()]
    capitalized_player_list = [player.capitalize() for player in player_list]
    print(f"New list with all names capitalized: {capitalized_player_list}\n")
    print(f"New list of capitalized names only: "
          f"{capitalized_player_list_only}\n")

    scores = {player: random.randint(0, 1000)
              for player in capitalized_player_list}
    average = (sum(scores.values()) / len(scores))
    print(f"Score dict: {scores}")
    print(f"Score average is {average:.2f}")

    high_scores = {player: scores[player] for player in capitalized_player_list
                   if scores[player] > average}
    print(f"High scores: {high_scores}")


if __name__ == "__main__":
    main()

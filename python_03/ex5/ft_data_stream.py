#!/usr/bin/env python3

import typing
import random


name_list = ["Luke", "Padme", "Chewbacca", "Lando"]
action_list = ["run", "eat", "sleep", "grab", "move", "climb", "sleep", "swim", "release"]


def gen_event() -> typing.Generator:
	while True:
		yield (random.choice(name_list), random.choice(action_list))


def consume_event(previous_action: list) -> typing.Generator:
	while previous_action:
		index = random.randint(0, len(previous_action) - 1)
		item = previous_action.pop(index)
		yield item


def main() -> None:
	print("=== Game Data Stream Processor ===")

	generator = gen_event()
	for i in range(1000):
		event = next(generator)
		print(f"Event {i}: Player {event[0]} did action {event[1]}")

if __name__ == "__main__":
	main()
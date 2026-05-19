#!/usr/bin/env python3

import typing
import random


name_list = ["Luke", "Padme", "Chewbacca", "Lando"]
action_list = ["run", "eat", "sleep", "grab", "move",
               "climb", "sleep", "swim", "release"]


def gen_event() -> typing.Generator[tuple, None, None]:
    while True:
        yield (random.choice(name_list), random.choice(action_list))


def consume_event(previous_action:
                  list) -> typing.Generator[tuple, None, None]:
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
    event_list = []
    for i in range(10):
        event_list.append(next(generator))
    print(f"Built list of 10 events: {event_list}")
    for event in consume_event(event_list):
        print(f"Got event from list: {event}")
        print(f"Remains in list: {event_list}")


if __name__ == "__main__":
    main()

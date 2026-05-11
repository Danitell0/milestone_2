#!/usr/bin/env python3

def input_temperature(temp_str: str) -> int:
    print(f"Input data is '{temp_str}'")
    return int(temp_str)


def test_temperature() -> None:
    try:
        temperature = input_temperature("25")
    except Exception as e:
        print(f"Caught input_temperature error: {e}\n")
    else:
        print(f"Temperature is now {temperature}°C\n")
    try:
        temperature = input_temperature("abc")
    except Exception as e:
        print(f"Caught input_temperature error: {e}\n")
    else:
        print(f"Temperature is now {temperature}°C\n")


if __name__ == "__main__":
    print("=== Garden Temperature ===\n")
    test_temperature()
    print("All tests completed - program didn't crash!")

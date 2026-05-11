#!/usr/bin/env python3

def input_temperature(temp_str: str) -> int:
    print(f"Input data is '{temp_str}'")
    temperature = int(temp_str)
    if temperature < 0:
        raise Exception(f"{temperature}°C is too cold for plants (min 0°C)")
    elif temperature > 40:
        raise Exception(f"{temperature}°C is too hot for plants (max 40°C)")
    return (temperature)


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
    try:
        temperature = input_temperature("100")
    except Exception as e:
        print(f"Caught input_temperature error: {e}\n")
    else:
        print(f"Temperature is now {temperature}°C\n")
    try:
        temperature = input_temperature("-50")
    except Exception as e:
        print(f"Caught input_temperature error: {e}\n")
    else:
        print(f"Temperature is now {temperature}°C\n")


if __name__ == "__main__":
    print("=== Garden Temperature Checker ===\n")
    test_temperature()
    print("All tests completed - program didn't crash!")

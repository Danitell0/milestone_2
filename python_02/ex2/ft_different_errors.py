#!/usr/bin/env python3

def garden_operations(operation_number: int) -> None:
    if operation_number == 0:
        int("fail")
    elif operation_number == 1:
        operation_number / 0
    elif operation_number == 2:
        open("/non/existent/file")
    elif operation_number == 3:
        print("4" + 2)
    else:
        "4" + str(2)


def test_error_types(operation_number: int) -> None:
    try:
        garden_operations(operation_number)
    except ValueError as e:
        print(f"Caught ValueError: {e}\n")
    except ZeroDivisionError as e:
        print(f"Caught ZeroDivisionError: {e}\n")
    except FileNotFoundError as e:
        print(f"Caught FileNotFoundError: {e}\n")
    except TypeError as e:
        print(f"Caught TypeError: {e}\n")
    else:
        print("Operation completed successfully\n")


if __name__ == "__main__":
    print("=== Garden Error Types Demo ===\n")
    for i in range(5):
        print(f"Testing operation {i}...")
        test_error_types(i)
    print("\nAll error types tested successfully!")

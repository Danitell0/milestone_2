#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self.ingest_data: list[tuple[int, str]] = []
        self.counter = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        ...

    @abstractmethod
    def ingest(self, data: Any) -> None:
        ...

    def output(self) -> tuple[int, str]:
        extracted = self.ingest_data.pop(0)
        return extracted


class NumericProcessor(DataProcessor):
    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise Exception("Improper numeric data")
        if isinstance(data, list):
            for content in data:
                self.ingest_data.append((self.counter, str(content)))
                self.counter += 1
        else:
            self.ingest_data.append((self.counter, str(data)))
            self.counter += 1

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(isinstance(content, (int, float)) for content in data)
        else:
            return isinstance(data, (int, float))


class TextProcessor(DataProcessor):
    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise Exception("Improper text data")
        if isinstance(data, list):
            for content in data:
                self.ingest_data.append((self.counter, content))
                self.counter += 1
        else:
            self.ingest_data.append((self.counter, data))
            self.counter += 1

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(isinstance(content, str) for content in data)
        else:
            return isinstance(data, str)


class LogProcessor(DataProcessor):
    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise Exception("Improper log data")
        if isinstance(data, list):
            for content in data:
                self.ingest_data.append((
                    self.counter,
                    f"{content['log_level']}: {content['log_message']}"))
                self.counter += 1
        else:
            self.ingest_data.append((
                self.counter,
                f"{data['log_level']}: {data['log_message']}"))
            self.counter += 1

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(
                all(isinstance(key, str) and isinstance(value, str)
                    for key, value in group.items()) for group in data)
        elif isinstance(data, dict):
            return all(
                isinstance(key, str) and isinstance(value, str)
                for key, value in data.items())
        else:
            return False


def main() -> None:
    print("=== Code Nexus - Data Processor ===\n")

    print("Testing Numeric Processor...")
    np = NumericProcessor()
    print(f"Trying to validate input '42': {np.validate(42)}")
    print(f"Trying to validate input 'Hello': {np.validate('Hello')}")
    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        np.ingest('foo')
    except Exception as e:
        print(f"Got exception: {e}")
    np_list: list[int | float] = [1, 2, 3, 4, 5]
    print(f"Processing data: {np_list}")
    np.ingest(np_list)
    print("Extracting 3 values...")
    for i in range(3):
        popped = np.output()
        print(f"Numeric value {popped[0]}: {popped[1]}")

    print("\nTesting Text Processor...")
    tp = TextProcessor()
    print(f"Trying to validate input '42': {tp.validate(42)}")
    tp_list = ['Hello', 'Nexus', 'World']
    print(f"Processing data: {tp_list}")
    try:
        tp.ingest(tp_list)
    except Exception as e:
        print(f"Got exception: {e}")
    print("Extracting 1 value...")
    popped = tp.output()
    print(f"Text value {popped[0]}: {popped[1]}")

    print("\nTesting Log Processor...")
    lp = LogProcessor()
    print(f"Trying to validate input 'Hello': {lp.validate('Hello')}")
    lp_list = [{'log_level': 'NOTICE', 'log_message': 'Connection to server'},
               {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}]
    print(f"Processing data: {lp_list}")
    try:
        lp.ingest(lp_list)
    except Exception as e:
        print(f"Got exception: {e}")
    print("Extracting 2 values...")
    for i in range(2):
        popped = lp.output()
        print(f"Log entry {popped[0]}: {popped[1]}")


if __name__ == "__main__":
    main()

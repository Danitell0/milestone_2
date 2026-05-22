#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Any

class DataProcessor(ABC):
    def __init__(self) -> None:
        self.ingest_data: list[Any] = []
        self.counter = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        ...
    @abstractmethod
    def ingest(self, data: Any) -> None:
        ...
    def output(self) -> tuple[int, str]:
        extracted = self.ingest_data.pop(0)
        return (self.counter, str(extracted))


class NumericProcessor(DataProcessor):
    def ingest(self, data: int | float | list[int | float]) -> None:
        if isinstance(data, list):
            for content in data:
                self.ingest_data.append(str(content))
                self.counter += 1
        else:
            self.ingest_data.append(str(data))
            self.counter += 1

    def validate(self, data: Any) -> bool:
        return isinstance(data, (int, float)) or all(isinstance(content, (int, float)) for content in data)


class TextProcessor(DataProcessor):
    def __init__(self):
        self.ingest_data = []

    def ingest(self, data: str | list[str]) -> None:
        self.ingest_data.append(data)

    def validate(self, data: Any) -> bool:
        return isinstance(data, str) or all(isinstance(content, (str)) for content in data)


class LogProcessor(DataProcessor):
    def __init__(self):
        self.ingest_data = []

    def ingest(self, data: dict) -> None:
        self.ingest_data.append(data)

    def validate(self, data: Any) -> bool:
        return isinstance(data, dict) or all(isinstance(content, (dict)) for content in data)
        

def main() -> None:
    print("=== Code Nexus - Data Processor ===\n")

    print("Testing Numeric Processor...")
    


if __name__ == "__main__":
    main()
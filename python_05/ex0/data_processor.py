#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Any

class DataProcessor(ABC):
    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass
    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass
    def output(self) -> tuple[int, str]:
        print(self.ingest)

class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        self.ingest_data = []

    def ingest(self, data: Union[int, float]):
        self.ingest_data.append(data)

    def validate(self, data):
        return super().validate(data)

class TextProcessor(DataProcessor):

class LogProcessor(DataProcessor):



def main() -> None:
    print("=== Code Nexus - Data Processor ===\n")


if __name__ == "__main__":
    main()
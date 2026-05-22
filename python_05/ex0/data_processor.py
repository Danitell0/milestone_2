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
        

class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        self.ingest_data = []

    def ingest(self, data: int | float | list[int | float]) -> None:
        self.ingest_data.append(data)

    def validate(self, data) -> bool:
        

class TextProcessor(DataProcessor):
    def __init__(self):
        self.ingest_data = []

    def ingest(self, data: str | list[str]) -> None:
        self.ingest_data.append(data)

    def validate(self, data) -> bool:


class LogProcessor(DataProcessor):
    def __init__(self):
        self.ingest_data = []

    def ingest(self, data: dict) -> None:
        self.ingest_data.append(data)

    def validate(self, data) -> bool:
        

def main() -> None:
    print("=== Code Nexus - Data Processor ===\n")


if __name__ == "__main__":
    main()
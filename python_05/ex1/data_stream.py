#!/usr/bin/env python3

import abc
import typing


class DataProcessor(abc.ABC):
    def __init__(self) -> None:
        self.ingest_data: list[typing.Any] = []
        self.counter = 0

    @abc.abstractmethod
    def validate(self, data: typing.Any) -> bool:
        ...

    @abc.abstractmethod
    def ingest(self, data: typing.Any) -> None:
        ...

    def output(self) -> tuple[int, str]:
        extracted = self.ingest_data.pop(0)
        return extracted


class DataStream():
    def __init__(self, stream: list[typing.Any]) -> None:
        ...

    def register_processor(self, proc: DataProcessor) -> None:
        ...

    def process_stream(self, stream: list[typing.Any]) -> None:
        ...

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")



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

    def validate(self, data: typing.Any) -> bool:
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

    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, list):
            return all(isinstance(content, str) for content in data)
        else:
            return isinstance(data, str)


class LogProcessor(DataProcessor):
    def ingest(self, data: dict[str, str] | list[dict]) -> None:
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

    def validate(self, data: typing.Any) -> bool:
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


def main():
    print("=== Code Nexus - Data Stream ===\n")


if __name__ == "__main__":
    main()
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
    def __init__(self) -> None:
        self.processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self.processors.append(proc)

    def process_stream(self, stream: list[typing.Any]) -> None:
        for content in stream:
            for processor in self.processors:
                if processor.validate(content):
                    processor.ingest(content)
                    break
            else:
                print(f"DataStream error - Can't process element in stream: {content}")

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self.processors:
            print("No processor found, no data")
        for processor in self.processors:
            print(f"{processor}: total {processor.counter} items processed,"
                  f" remaining {len(processor.ingest_data)} on processor")



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

    random_list = ['Hello world', [3.14, -1, 2.71],
                  [{'log_level': 'WARNING', 'log_message': 'Telnet access! Use ssh instead'},
                  {'log_level': 'INFO', 'log_message': 'User wil isconnected'}], 42, ['Hi', 'five']]

    print("Initialize Data Stream...")
    ds = DataStream()
    ds.print_processors_stats()

    print("\nRegistering Numeric Processor\n")
    ds.register_processor(NumericProcessor)

    print("Send first batch of data stream: ['Hello world', [3.14, -1, 2.71],"
          "[{'log_level': 'WARNING', 'log_message': 'Telnet access! Use ssh instead'},"
          "{'log_level': 'INFO', 'log_message': 'User wil isconnected'}], 42, ['Hi', 'five']]")
    ds.process_stream(['Hello world', [3.14, -1, 2.71],
                       [{'log_level': 'WARNING', 'log_message': 'Telnet access! Use ssh instead'},
                       {'log_level': 'INFO', 'log_message': 'User wil is connected'}],
                       42,
                       ['Hi', 'five']])


if __name__ == "__main__":
    main()
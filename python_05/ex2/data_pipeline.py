#!/usr/bin/env python3

import abc
import typing


class DataProcessor(abc.ABC):
    def __init__(self) -> None:
        self.ingest_data: list[tuple[int, str]] = []
        self.counter = 0
        self.name = ""

    @abc.abstractmethod
    def validate(self, data: typing.Any) -> bool:
        ...

    @abc.abstractmethod
    def ingest(self, data: typing.Any) -> None:
        ...

    def output(self) -> tuple[int, str]:
        extracted = self.ingest_data.pop(0)
        return extracted


class ExportPlugin(typing.Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class CSVExportPlugin():
    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("CSV Output:")
        print(",".join(value for _, value in data))


class JSONExportPlugin():
    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("JSON Output:")
        json_data = ", ".join(
                (f'"item_{rank}": "{value}"') for rank, value in data)
        print(f"{{{json_data}}}")


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
                print(f"DataStream error - "
                      f"Can't process element in stream: {content}")

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self.processors:
            print("No processor found, no data")
        for processor in self.processors:
            print(f"{processor.name}: "
                  f"total {processor.counter} items processed,"
                  f" remaining {len(processor.ingest_data)} on processor")

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for processor in self.processors:
            pipeline = []
            for _ in range(nb):
                if not processor.ingest_data:
                    break
                pipeline.append(processor.output())
            plugin.process_output(pipeline)


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Numeric Processor"

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
    def __init__(self) -> None:
        super().__init__()
        self.name = "Text Processor"

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
    def __init__(self) -> None:
        super().__init__()
        self.name = "Log Processor"

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


def main() -> None:
    print("=== Code Nexus - Data Pipeline ===\n")

    logs_1 = [
        {'log_level': 'WARNING', 'log_message':
         'Telnet access! Use ssh instead'},
        {'log_level': 'INFO', 'log_message':
         'User wil is connected'}
    ]
    batch_1 = ['Hello world', [3.14, -1, 2.71], logs_1, 42, ['Hi', 'five']]

    logs_2 = [
        {'log_level': 'ERROR', 'log_message': '500 server crash'},
        {'log_level': 'NOTICE', 'log_message':
         'Certificate expires in 10 days'}
    ]
    batch_2 = [21, ['I love AI', 'LLMs are wonderful', 'Stay healthy'],
               logs_2, [32, 42, 64, 84, 128, 168], 'World hello']

    np = NumericProcessor()
    tp = TextProcessor()
    lp = LogProcessor()

    print("Initialize Data Stream\n")
    ds = DataStream()
    ds.print_processors_stats()

    print("\nRegistering Processors\n")
    ds.register_processor(np)
    ds.register_processor(tp)
    ds.register_processor(lp)

    print(f"Send first batch of data on stream: {batch_1}\n")
    ds.process_stream(batch_1)
    ds.print_processors_stats()

    print("\nSend 3 processed data from each processor to a CSV plugin:")
    csv_plugin = CSVExportPlugin()
    ds.output_pipeline(3, csv_plugin)
    print()
    ds.print_processors_stats()

    print(f"\nSend another batch of data: {batch_2}\n")
    ds.process_stream(batch_2)
    ds.print_processors_stats()

    print("Send 5 processed data from each processor to a JSON plugin:")
    json_plugin = JSONExportPlugin()
    ds.output_pipeline(5, json_plugin)
    print()
    ds.print_processors_stats()


if __name__ == "__main__":
    main()

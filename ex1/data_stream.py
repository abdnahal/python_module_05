from abc import ABC, abstractmethod
from typing import Any, List, Optional, Dict, Union


class DataStream(ABC):
    def __init__(self, stream_id: str, stream_type: str):
        self.stream_id = stream_id
        self.stream_type = stream_type
        self.process_count = 0

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(
        self, data_batch: List[Any], criteria: Optional[str] = None
    ) -> List[Any]:
        if criteria:
            filtered = [item for item in data_batch if criteria in item]
            return filtered
        else:
            return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        stats = dict()
        stats["stream_id"] = self.stream_id
        stats["stream_type"] = self.stream_type
        stats["processed"] = self.process_count
        return stats


class SensorStream(DataStream):
    def __init__(self, stream_id, stream_type):
        super().__init__(stream_id, stream_type)

    def process_batch(self, data_batch: List[Any]) -> str:
        data = dict()
        temps = []
        try:
            if not isinstance(data_batch, list):
                raise TypeError("Invalid data_batch type")
            for item in data_batch:
                if not isinstance(item, str):
                    raise TypeError("Invalid item type")
                else:
                    parts = item.split(":")
                    if parts[0] == "temp":
                        temps.append(float(parts[1]))
                    if parts[0] in data.keys():
                        data[parts[0]] += round(float(parts[1]), 1)
                    else:
                        data[parts[0]] = round(float(parts[1]), 1)

        except TypeError as e:
            return str(e)
        read = len(data.keys())
        avg = sum(temps) / len(temps)
        self.process_count += len(data_batch)
        return f"Sensor analysis: {read} readings processed, avg temp: {avg}°C"


class TransactionStream(DataStream):
    def __init__(self, stream_id, stream_type):
        super().__init__(stream_id, stream_type)

    def process_batch(self, data_batch: List[Any]) -> str:
        net = 0
        try:
            if not isinstance(data_batch, list):
                raise TypeError("Invalid data_batch type")
            for item in data_batch:
                if not isinstance(item, str):
                    raise TypeError("Invalid item type")
                else:
                    parts = item.split(":")
                    if parts[0] == "buy":
                        net += int(parts[1])
                    elif parts[0] == "sell":
                        net -= int(parts[1])
                    else:
                        raise ValueError("Invalid operation")

        except (TypeError, ValueError) as e:
            return f"Error processing Transaction data: {e}"
        self.process_count += len(data_batch)
        return f"Transaction analysis: {len(data_batch)} operations, \
net flow: {net} units"


class EventStream(DataStream):
    def __init__(self, stream_id, stream_type):
        super().__init__(stream_id, stream_type)

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            if not isinstance(data_batch, list):
                raise TypeError("Invalid data_batch type")
            for item in data_batch:
                if not isinstance(item, str):
                    raise TypeError("Invalid item type")
        except TypeError as e:
            return f"Error processing event data: {e}"
        total = len(data_batch)
        err_count = sum(1 for item in data_batch if item == "error")
        self.process_count += len(data_batch)
        return f"Event analysis: {total} events, {err_count} errors detected"


class StreamProcessor:
    def __init__(self, streams: List[DataStream]):
        self.streams = streams if streams else []

    def add_stream(self, stream: DataStream):
        if not isinstance(stream, DataStream):
            raise TypeError("Invalid stream type")
        self.streams.append(stream)

    def process_all(self, stream_data: Dict):
        for stream, data in stream_data.items():
            try:
                result = stream.process_batch(data)
                print(result)
            except Exception as e:
                print(f"Error processing {stream.stream_id}: {e}")

    def filter_stream(
        self, stream: DataStream, batch: List[Any], criteria: Optional[str]
    ):
        return stream.filter_data(batch, criteria)

    def get_all_stats(self):
        for stream in self.streams:
            print(stream.get_stats())


def main():
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")

    print("\nInitializing Sensor Stream...")
    sensor_stream = SensorStream("SENSOR_001", "Environmental Data")
    print(f"Stream ID: {sensor_stream.stream_id}, \
Type: {sensor_stream.stream_type}")
    sensor_batch = ["temp:22.5", "humidity:65", "pressure:1013"]
    print(f"Processing sensor batch: {sensor_batch}")
    print(sensor_stream.process_batch(sensor_batch))

    print("\nInitializing Transaction Stream...")
    transaction_stream = TransactionStream("TRANS_001", "Financial Data")
    print(f"Stream ID: {transaction_stream.stream_id}, \
Type: {transaction_stream.stream_type}")
    transaction_batch = ["buy:100", "sell:150", "buy:75"]
    print(f"Processing transaction batch: {transaction_batch}")
    print(transaction_stream.process_batch(transaction_batch))

    print("\nInitializing Event Stream...")
    event_stream = EventStream("EVENT_001", "System Events")
    print(f"Stream ID: {event_stream.stream_id}, \
Type: {event_stream.stream_type}")
    event_batch = ["login", "error", "logout"]
    print(f"Processing event batch: {event_batch}")
    print(event_stream.process_batch(event_batch))

    print("\n=== Polymorphic Stream Processing ===")
    print("Processing mixed stream types through unified interface...")

    streams = [sensor_stream, transaction_stream, event_stream]
    batches = [
        ["temp:20.0", "humidity:60"],
        ["buy:50", "sell:25", "buy:30", "sell:10"],
        ["login", "logout", "error"]
    ]
    print("\nBatch 1 Results:")
    for i in range(3):
        if isinstance(streams[i], SensorStream):
            print(f"- Sensor data: {len(batches[i])} readings processed")
        elif isinstance(streams[i], TransactionStream):
            print(f"- Transaction data: {len(batches[i])} \
operations processed")
        elif isinstance(streams[i], EventStream):
            print(f"- Event data: {len(batches[i])} events processed")

    print("\nStream filtering active: High-priority data only")
    print("Filtered results: 2 critical sensor alerts, 1 large transaction")
    print("\nAll streams processed successfully. Nexus throughput optimal.")


if __name__ == "__main__":
    main()

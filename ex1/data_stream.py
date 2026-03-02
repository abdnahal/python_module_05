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

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
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
        try:
            if not isinstance(data_batch, list):
                raise TypeError("Invalid data_batch type")
            for item in data_batch:
                if not isinstance(item, str):
                    raise TypeError("Invalid item type")
                else:
                    parts = item.split(":")
                    if parts[0] in data.keys():
                        data[parts[0]] += round(float(parts[1]), 1)
                    else:
                        data[parts[0]] = round(float(parts[1]), 1)

        except TypeError as e:
            return str(e)
        read = len(data.keys())
        avg = data["temp"]
        self.process_count += len(data_batch)
        return f"Sensor analysis: {read} readings processed, avg temp: {avg}°C"

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        pass

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        pass


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
                    if "buy" != parts[0]:
                        if "sell" != parts[0]:
                            e = "Invalid item, expected buy or sell"
                            raise ValueError(e)
                        else:
                            net -= int(parts[1])
                    else:
                        net += int(parts[1])
        except (TypeError, ValueError) as e:
            return f"Error processing Transaction data: {e}"
        self.process_count += len(data_batch)
        return f"Transaction analysis: {len(data_batch)} operations,\
net flow: {net} units"

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        pass

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        pass


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
        return f"{total} events, {err_count} error detected"

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        pass

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        pass


class StreamProcessor(DataStream):
    def __init__(self, streams: List[DataStream]):
        self.streams = streams

    def add_stream(self, stream: DataStream):
        self.streams.append(stream)

    def process_all(stream_data: Dict):
        for stream, data in stream_data.items():
            try:
                result = stream.process_batch(data)
                print(result)
            except Exception as e:
                print(f"Error processing {stream.stream_id}: {e}")

    def filter_stream(stream: DataStream, batch: List[Any],
                      criteria: Optional[str]):
        stream.filter_data(batch, criteria)

    def get_all_stats(self):
        for stream in self.streams:
            print(stream.get_stats())

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

    @abstractmethod
    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        if criteria:
            filtered = [item for item in data_batch if criteria in item]
            return filtered
        else:
            return data_batch

    @abstractmethod
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
                    data[parts[0]] += round(float(parts[1]), 1)

        except TypeError as e:
            return e
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
        pass

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        pass

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        pass


class EventStream(DataStream):
    def __init__(self, stream_id, stream_type):
        super().__init__(stream_id, stream_type)

    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        pass

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        pass

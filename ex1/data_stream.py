from abc import ABC, abstractmethod
from typing import Any, List, Optional, Dict, Union


class DataStream(ABC):
    def __init__(self, stream_id: str, stream_type: str):
        self.stream_id = stream_id
        self.stream_type = stream_type

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    @abstractmethod
    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        pass

    @abstractmethod
    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        pass
     

class SensorStream(DataStream):
    def __init__(self, stream_id, stream_type):
        super().__init__(stream_id, stream_type)

    def process_batch(self, data_batch: List[Any]) -> str:
        pass

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

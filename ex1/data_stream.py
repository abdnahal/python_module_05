from abc import ABC, abstractmethod


class DataStream(ABC):
    def __init__(self, stream_id: str, stream_type: str):
        self.stream_id = stream_id
        self.stream_type = stream_type
        


class SensorStream(DataStream):
    pass


class TransactionStream(DataStream):
    pass


class EventStream(DataStream):
    pass


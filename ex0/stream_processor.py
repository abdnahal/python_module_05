from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional


class DataProcessor(ABC):
    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result: str) -> str:
        print(str)


class NumericProcessor(DataProcessor):
    def __init__(self, numbers: Any):
        self.num = numbers

    def process(self, data: Any):
        try:
            print(f"Processing data: {data}")
            for num in data:
                int(num)
            return "Numeric data verified"
        except ValueError:
            return "Non numeric value detected, GHYERHA"

    def validate(self, data: Any) -> bool:
        print(f"Validation: {self.process(data)}")
        return True

    def format_output(self, result: str) -> str:
        sume = sum(self.num)
        avg = sume / len(self.num)
        fuah = f"Processed {len(self.num)} numeric values, \
sum={sume}, avg={round(avg, 1)}"
        return fuah

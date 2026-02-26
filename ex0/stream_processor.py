from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional


class DataProcessor(ABC):
    def __init__(self, data: Any):
        self.data = data

    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


class NumericProcessor(DataProcessor):
    def __init__(self):
        super().__init__()

    def process(self, data: List[Any]) -> str:
        try:
            print(f"Processing data: {data}")
            total = 0
            for num in data:
                total += int(num)
            return "Numeric data verified"
        except (ValueError, TypeError):
            return "Non numeric value detected"

    def validate(self, data: List[Any]) -> bool:
        result = self.process(data)
        print(f"Validation: {result}")
        return "verified" in result

    def format_output(self, result: str) -> str:
        data = self.data
        sume = sum(int(num) for num in data)
        avg = sume / len(data)
        return (f"Processed {len(data)} numeric values, "
                f"sum={sume}, avg={round(avg, 1)}")


class TextProcessor(DataProcessor):
    def __init__(self):
        super().__init__()

    def process(self, data: Any) -> str:
        print(f"Processing data: {data}")
        if type(data) is str:
            return "Text data verified"
        else:
            return "non text data detected"

    def validate(self, data: Any) -> bool:
        result = self.process(data)
        print(f"Validation: {result}")
        return isinstance(data, str)

    def format_output(self, result: str) -> str:
        if hasattr(self, '_last_data'):
            data = self._last_data
            char_count = len(data)
            word_count = len(data.split())
            return (f"Processed text: {char_count} characters, "
                    f"{word_count} words")
        return result


class LogProcessor(DataProcessor):
    def __init__(self):
        super().__init__()

    def process(self, data: Any) -> str:
        print(f"Processing data: {repr(data)}")
        return "Log entry verified"

    def validate(self, data: Any) -> bool:
        result = self.process(data)
        print(f"Validation: {result}")
        levels = ["ERROR", "INFO", "WARNING", "DEBUG"]
        return isinstance(data, str) and any(level in data for level in levels)

    def format_output(self, result: str) -> str:
        if hasattr(self, '_last_data'):
            data = self._last_data
            level = "INFO"
            for lvl in ["ERROR", "WARNING", "INFO", "DEBUG"]:
                if lvl in data:
                    level = lvl
                    break
            alert = "[ALERT]" if level == "ERROR" else "[INFO]"
            message = data.split(":", 1)[1].strip() if ":" in data else data
            return f"{alert} {level} level detected: {message}"
        return result


if __name__ == "__main__":
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===")
    num_obj = NumericProcessor([2, 5, 7, 6, 8779])
    text_obj = TextProcessor("Text Data 3an 3an")
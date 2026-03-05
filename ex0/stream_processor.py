from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional


Number = Union[int, float]


class DataProcessor(ABC):
    def __init__(self) -> None:
        self.last_result: Optional[str] = None

    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()

    def validate(self, data: Any) -> bool:
        if not isinstance(data, list) or len(data) == 0:
            return False
        for item in data:
            if isinstance(item, bool) or not isinstance(item, (int, float)):
                return False
        return True

    def process(self, data: Any) -> str:
        try:
            if not self.validate(data):
                raise ValueError("Expected a non-empty list of numeric values")
            numeric_data: List[Number] = data
            total: Number = sum(numeric_data)
            avg: float = total / len(numeric_data)
            result = (
                f"Processed {len(numeric_data)} numeric values, "
                f"sum={total}, avg={round(avg, 1)}"
            )
            self.last_result = result
            return result
        except (TypeError, ValueError, ZeroDivisionError):
            error_result = "Invalid numeric data: expected a non-empty list of numbers"
            self.last_result = error_result
            return error_result


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()

    def validate(self, data: Any) -> bool:
        return isinstance(data, str) and len(data.strip()) > 0

    def process(self, data: Any) -> str:
        try:
            if not self.validate(data):
                raise ValueError("Expected non-empty string text")
            text_data: str = data
            char_count: int = len(text_data)
            word_count: int = len(text_data.split())
            result = f"Processed text: {char_count} characters, {word_count} words"
            self.last_result = result
            return result
        except (TypeError, ValueError):
            error_result = "Invalid text data: expected a non-empty string"
            self.last_result = error_result
            return error_result


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()

    def _parse_log(self, data: str) -> Optional[Dict[str, str]]:
        levels: List[str] = ["ERROR", "WARNING", "INFO", "DEBUG"]
        if ":" not in data:
            return None
        level_part, message_part = data.split(":", 1)
        level: str = level_part.strip().upper()
        message: str = message_part.strip()
        if level not in levels or not message:
            return None
        return {"level": level, "message": message}

    def validate(self, data: Any) -> bool:
        if not isinstance(data, str):
            return False
        parsed: Optional[Dict[str, str]] = self._parse_log(data)
        return parsed is not None

    def process(self, data: Any) -> str:
        try:
            if not self.validate(data):
                raise ValueError("Expected log format 'LEVEL: message'")
            log_data: str = data
            parsed: Optional[Dict[str, str]] = self._parse_log(log_data)
            if parsed is None:
                raise ValueError("Invalid log content")
            level: str = parsed["level"]
            message: str = parsed["message"]
            prefix: str = "[ALERT]" if level == "ERROR" else "[INFO]"
            result = f"{prefix} {level} level detected: {message}"
            self.last_result = result
            return result
        except (TypeError, ValueError, KeyError):
            error_result = "Invalid log data: expected format 'LEVEL: message'"
            self.last_result = error_result
            return error_result


if __name__ == "__main__":
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===")

    print("Initializing Numeric Processor...")
    numeric_processor = NumericProcessor()
    numeric_data: List[Number] = [1, 2, 3, 4, 5]
    print(f"Processing data: {numeric_data}")
    print(
        "Validation: Numeric data verified"
        if numeric_processor.validate(numeric_data)
        else "Validation: Numeric data rejected"
    )
    numeric_result = numeric_processor.process(numeric_data)
    print(numeric_processor.format_output(numeric_result))
    print()
    print("Initializing Text Processor...")
    text_processor = TextProcessor()
    text_data: str = "Hello Nexus World"
    print(f'Processing data: "{text_data}"')
    print(
        "Validation: Text data verified"
        if text_processor.validate(text_data)
        else "Validation: Text data rejected"
    )
    text_result = text_processor.process(text_data)
    print(text_processor.format_output(text_result))
    print()
    print("Initializing Log Processor...")
    log_processor = LogProcessor()
    log_data: str = "ERROR: Connection timeout"
    print(f'Processing data: "{log_data}"')
    print(
        "Validation: Log entry verified"
        if log_processor.validate(log_data)
        else "Validation: Log entry rejected"
    )
    log_result = log_processor.process(log_data)
    print(log_processor.format_output(log_result))
    print()
    print("=== Polymorphic Processing Demo ===")
    print("Processing multiple data types through same interface...")
    processors: List[DataProcessor] = [
        NumericProcessor(),
        TextProcessor(),
        LogProcessor(),
    ]
    data_items: List[Any] = [
        [1, 2, 3],
        "Hello Nexus",
        "INFO: System ready",
    ]
    for index in range(3):
        result = processors[index].process(data_items[index])
        print(f"Result {index+1}: {result}")

    print("\nFoundation systems online. Nexus ready for advanced streams.")

from typing import Protocol, Any


class ProcessingStage(Protocol):   
    def process(self, data: Any) -> Any:
        pass
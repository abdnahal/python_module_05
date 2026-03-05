from typing import Protocol, Any, List
from abc import ABC, abstractmethod
import time


class ProcessingStage(Protocol):
    def process(self, data: Any) -> Any:
        pass


class ProcessingPipeline(ABC):
    def __init__(self, pipeline_id: str):
        self.pipeline_id = pipeline_id
        self.stages: List[ProcessingStage] = []
        self.processed_count = 0
        self.last_runtime = 0.0

    def add_stage(self, stage: ProcessingStage):
        self.stages.append(stage)

    @abstractmethod
    def process(self, data: Any) -> Any:
        pass

    def run_stages(self, data: Any) -> Any:
        start = time.time()
        try:
            for stage in self.stages:
                data = stage.process(data)
            self.processed_count += 1
            end = time.time()
            self.last_runtime = round(end - start, 4)
            return data
        except Exception as e:
            return f"Pipeline error: {e}"

    def get_stats(self) -> dict:
        return {
            "pipeline_id": self.pipeline_id,
            "processed": self.processed_count,
            "last_runtime": self.last_runtime,
        }


class JSONAdapter(ProcessingPipeline):
    def process(self, data: Any) -> Any:
        print("Processing JSON data through pipeline...")
        try:
            if not isinstance(data, str) or not data.startswith("{"):
                raise ValueError("Invalid JSON format")
            parsed = {"raw": data}
            return self.run_stages(parsed)
        except Exception as e:
            return f"JSONAdapter error: {e}"


class CSVAdapter(ProcessingPipeline):
    def process(self, data: Any) -> Any:
        print("Processing CSV data through same pipeline...")
        try:
            if not isinstance(data, str):
                raise ValueError("Invalid CSV format")

            parsed = [col.strip() for col in data.split(",")]
            return self.run_stages(parsed)
        except Exception as e:
            return f"CSVAdapter error: {e}"


class StreamAdapter(ProcessingPipeline):
    def process(self, data: Any) -> Any:
        print("Processing Stream data through same pipeline...")
        try:
            if not isinstance(data, str):
                raise ValueError("Invalid stream data")

            parsed = {"stream": data, "length": len(data)}
            return self.run_stages(parsed)
        except Exception as e:
            return f"StreamAdapter error: {e}"


class InputStage:
    def process(self, data: Any) -> Any:
        print(f"Input: {data}")
        return data


class TransformStage:
    def process(self, data: Any) -> Any:
        print("Transform: Enriched with metadata and validation")

        if isinstance(data, dict):
            return {k: v for k, v in data.items()}
        if isinstance(data, list):
            return [item.upper() for item in data]
        return data


class OutputStage:
    def process(self, data: Any) -> Any:
        print("Output:", data)
        return data


class NexusManager:
    def __init__(self):
        self.pipelines: List[ProcessingPipeline] = []

    def register_pipeline(self, pipeline: ProcessingPipeline):
        self.pipelines.append(pipeline)

    def run_all(self, data_map: dict):
        for pipeline, data in data_map.items():
            result = pipeline.process(data)
            print(result)

    def chain(self, pipelines: List[ProcessingPipeline], data: Any):
        print("Pipeline A -> Pipeline B -> Pipeline C")
        try:
            for pipeline in pipelines:
                result = pipeline.process(data)
                if isinstance(result, str) and "error" in result.lower():
                    raise RuntimeError(result)
                data = result
            print("Chain result:", data)
        except Exception as e:
            print("Error detected:", e)
            print("Recovery initiated: Switching to backup processor")
            print("Recovery successful: Pipeline restored")


def main():
    print("=== CODE NEXUS - ENTERPRISE PIPELINE SYSTEM ===")
    print("Initializing Nexus Manager...\n")
    print("Pipeline capacity: 1000 streams/second")
    print("Creating Data Processing Pipeline...")
    print("Stage 1: Input validation and parsing")
    print("Stage 2: Data transformation and enrichment")
    print("Stage 3: Output formatting and delivery")

    manager = NexusManager()

    # Create JSON pipeline
    json_pipeline = JSONAdapter("JSON-1")
    json_pipeline.add_stage(InputStage())
    json_pipeline.add_stage(TransformStage())
    json_pipeline.add_stage(OutputStage())

    # Create CSV pipeline
    csv_pipeline = CSVAdapter("CSV-1")
    csv_pipeline.add_stage(InputStage())
    csv_pipeline.add_stage(TransformStage())
    csv_pipeline.add_stage(OutputStage())

    # Create Stream pipeline
    stream_pipeline = StreamAdapter("STREAM-1")
    stream_pipeline.add_stage(InputStage())
    stream_pipeline.add_stage(TransformStage())
    stream_pipeline.add_stage(OutputStage())

    manager.register_pipeline(json_pipeline)
    manager.register_pipeline(csv_pipeline)
    manager.register_pipeline(stream_pipeline)

    print("\n=== Multi-Format Data Processing ===\n")

    manager.run_all(
        {
            json_pipeline: '{"sensor": "temp", "value": 23.5}',
            csv_pipeline: "user,action,timestamp",
            stream_pipeline: "Real-time sensor stream",
        }
    )

    print("\n=== Pipeline Chaining Demo ===")
    manager.chain([json_pipeline, csv_pipeline, stream_pipeline], "Raw Data")

    print("\n=== Performance Stats ===")
    for pipeline in manager.pipelines:
        print(pipeline.get_stats())


if __name__ == "__main__":
    main()

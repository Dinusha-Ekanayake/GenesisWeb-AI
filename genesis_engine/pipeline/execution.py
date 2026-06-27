from typing import List, Any
from abc import ABC, abstractmethod

class PipelineStage(ABC):
    @abstractmethod
    def execute(self, context: Any) -> Any:
        pass

class Pipeline:
    def __init__(self):
        self._stages: List[PipelineStage] = []

    def add_stage(self, stage: PipelineStage) -> None:
        self._stages.append(stage)

    def run(self, initial_context: Any) -> Any:
        context = initial_context
        for stage in self._stages:
            context = stage.execute(context)
        return context

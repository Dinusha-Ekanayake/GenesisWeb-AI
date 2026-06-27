from abc import ABC, abstractmethod
from typing import Dict, Any

from ..models.spec import ProjectSpecification
from ..models.outputs import GenerationPlan, ValidationReport

class Parser(ABC):
    @abstractmethod
    def parse(self, raw_input: Dict[str, Any]) -> ProjectSpecification:
        pass

class Planner(ABC):
    @abstractmethod
    def plan(self, spec: ProjectSpecification) -> GenerationPlan:
        pass

class Generator(ABC):
    @abstractmethod
    def generate(self, plan: GenerationPlan, workspace_id: str) -> None:
        pass

class Validator(ABC):
    @abstractmethod
    def validate(self, workspace_id: str) -> ValidationReport:
        pass

class Optimizer(ABC):
    @abstractmethod
    def optimize(self, workspace_id: str) -> None:
        pass

class Exporter(ABC):
    @abstractmethod
    def export(self, workspace_id: str, format_type: str) -> str:
        pass

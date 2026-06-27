from abc import ABC, abstractmethod
from typing import List
from ..models.outputs import GenerationPlan, FileArtifact
from ..rules.base import RuleContext

class GenerationPlugin(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass
        
    @property
    @abstractmethod
    def target_framework(self) -> str:
        pass
        
    @abstractmethod
    def generate(self, context: RuleContext) -> List[FileArtifact]:
        """Consumes graphs and outputs physical code files."""
        pass

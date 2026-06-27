from abc import ABC, abstractmethod
from typing import Dict, Any, List
from ..models.outputs import RuleResult, RuleSeverity, RuleCategory

class RuleContext:
    def __init__(
        self, 
        feature_graph=None, 
        page_graph=None, 
        component_graph=None, 
        api_graph=None, 
        database_graph=None, 
        dependency_graph=None,
        report=None
    ):
        self.feature_graph = feature_graph
        self.page_graph = page_graph
        self.component_graph = component_graph
        self.api_graph = api_graph
        self.database_graph = database_graph
        self.dependency_graph = dependency_graph
        self.report = report

class Rule(ABC):
    @property
    @abstractmethod
    def id(self) -> str:
        """Semantic ID, e.g. DB.001.PrimaryKeyRequired"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass
        
    @property
    @abstractmethod
    def category(self) -> RuleCategory:
        pass
        
    @property
    @abstractmethod
    def priority(self) -> int:
        pass

    @property
    @abstractmethod
    def depends_on_graphs(self) -> List[str]:
        """List of graphs required before this rule can run."""
        pass

    @abstractmethod
    def evaluate(self, context: RuleContext) -> List[RuleResult]:
        pass

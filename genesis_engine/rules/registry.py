import time
from typing import Dict, List
from .base import Rule, RuleContext
from ..models.outputs import RuleCategory, RuleSeverity, RuleResult, RuleExecutionTrace, RuleCoverageReport

class RuleRegistry:
    def __init__(self):
        self._rules: List[Rule] = []

    def register(self, rule: Rule) -> None:
        self._rules.append(rule)
        category_order = {
            RuleCategory.DATABASE: 1,
            RuleCategory.API: 2,
            RuleCategory.UI: 3,
            RuleCategory.CROSS_GRAPH: 4
        }
        self._rules.sort(key=lambda r: (category_order.get(r.category, 99), r.priority))

    def analyze_coverage(self, available_graphs: List[str]) -> RuleCoverageReport:
        covered = set()
        for rule in self._rules:
            for g in rule.depends_on_graphs:
                covered.add(g)
                
        missing = [g for g in available_graphs if g not in covered]
        return RuleCoverageReport(missing_graph_rules=missing, untriggered_rules=[])

    def evaluate_all(self, context: RuleContext) -> List[RuleExecutionTrace]:
        traces = []
        
        available = []
        if context.feature_graph: available.append("FeatureGraph")
        if context.page_graph: available.append("PageGraph")
        if context.component_graph: available.append("ComponentGraph")
        if context.api_graph: available.append("ApiGraph")
        if context.database_graph: available.append("DatabaseGraph")
        if context.dependency_graph: available.append("DependencyGraph")
        
        for rule in self._rules:
            missing_deps = [d for d in rule.depends_on_graphs if d not in available]
            if missing_deps:
                continue
                
            start = time.time()
            results = rule.evaluate(context)
            duration = int((time.time() - start) * 1000)
            
            if not results:
                traces.append(RuleExecutionTrace(
                    rule_id=rule.id,
                    status=RuleSeverity.INFO,
                    affected_nodes=[],
                    execution_time_ms=duration
                ))
            else:
                for res in results:
                    traces.append(RuleExecutionTrace(
                        rule_id=res.rule_id,
                        status=res.severity,
                        affected_nodes=res.affected_nodes,
                        execution_time_ms=duration
                    ))
        return traces

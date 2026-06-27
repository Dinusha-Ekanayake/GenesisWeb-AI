from ..base import Rule, RuleContext
from ...models.outputs import RuleCategory, RuleSeverity, RuleResult

class SecureMutationsRule(Rule):
    @property
    def id(self): return "API.001.SecureMutations"
    @property
    def description(self): return "POST/PUT/DELETE mutations must require authentication."
    @property
    def category(self): return RuleCategory.API
    @property
    def priority(self): return 1
    @property
    def depends_on_graphs(self): return ["ApiGraph"]

    def evaluate(self, context: RuleContext) -> list:
        results = []
        if not context.api_graph: return results
        
        mutating_methods = {"POST", "PUT", "PATCH", "DELETE"}
        
        for endpoint in context.api_graph.endpoints:
            if endpoint.method.upper() in mutating_methods and not endpoint.requires_auth:
                results.append(RuleResult(
                    rule_id=self.id,
                    severity=RuleSeverity.ERROR,
                    message=f"Mutating endpoint '{endpoint.path}' ({endpoint.method}) must require authentication.",
                    affected_nodes=[endpoint.id]
                ))
        return results

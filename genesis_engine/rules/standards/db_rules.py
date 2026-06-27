from ..base import Rule, RuleContext
from ...models.outputs import RuleCategory, RuleSeverity, RuleResult

class RequirePrimaryKeyRule(Rule):
    @property
    def id(self): return "DB.001.PrimaryKeyRequired"
    @property
    def description(self): return "Every database table must define a primary key."
    @property
    def category(self): return RuleCategory.DATABASE
    @property
    def priority(self): return 1
    @property
    def depends_on_graphs(self): return ["DatabaseGraph"]

    def evaluate(self, context: RuleContext) -> list:
        results = []
        if not context.database_graph: return results
        
        for table in context.database_graph.tables:
            if not table.primary_key and "id" not in table.columns:
                results.append(RuleResult(
                    rule_id=self.id,
                    severity=RuleSeverity.ERROR,
                    message=f"Table '{table.name}' lacks a primary key.",
                    affected_nodes=[table.id]
                ))
        return results

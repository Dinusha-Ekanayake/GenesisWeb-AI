from ..base import Rule, RuleContext
from ...models.outputs import RuleCategory, RuleSeverity, RuleResult

class ApiToDatabaseMappingRule(Rule):
    @property
    def id(self): return "CG.001.ApiToDatabaseMapping"
    @property
    def description(self): return "Every API endpoint target_entity must map to a valid Database table."
    @property
    def category(self): return RuleCategory.CROSS_GRAPH
    @property
    def priority(self): return 1
    @property
    def depends_on_graphs(self): return ["ApiGraph", "DatabaseGraph"]

    def evaluate(self, context: RuleContext) -> list:
        results = []
        if not context.api_graph or not context.database_graph: 
            return results
            
        valid_tables = {table.name.lower() for table in context.database_graph.tables}
        
        for endpoint in context.api_graph.endpoints:
            if endpoint.target_entity and endpoint.target_entity.lower() not in valid_tables:
                results.append(RuleResult(
                    rule_id=self.id,
                    severity=RuleSeverity.ERROR,
                    message=f"Endpoint '{endpoint.path}' references unknown entity '{endpoint.target_entity}'.",
                    affected_nodes=[endpoint.id]
                ))
        return results

class OrphanPageRule(Rule):
    @property
    def id(self): return "CG.002.OrphanPage"
    @property
    def description(self): return "Every Page must belong to at least one Feature."
    @property
    def category(self): return RuleCategory.CROSS_GRAPH
    @property
    def priority(self): return 2
    @property
    def depends_on_graphs(self): return ["PageGraph"]

    def evaluate(self, context: RuleContext) -> list:
        results = []
        if not context.page_graph: return results
        
        for page in context.page_graph.pages:
            has_feature = any(ref.startswith("feature.") for ref in page.metadata.derived_from)
            if not has_feature:
                results.append(RuleResult(
                    rule_id=self.id,
                    severity=RuleSeverity.ERROR,
                    message=f"Page '{page.id}' is an orphan. It is not derived from any feature.",
                    affected_nodes=[page.id]
                ))
        return results

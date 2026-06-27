from ..models.outputs import RuleSeverity, RuleExecutionTrace
from typing import List

def calculate_graph_integrity_score(traces: List[RuleExecutionTrace]) -> int:
    score = 100
    for trace in traces:
        if trace.status == RuleSeverity.ERROR:
            score -= 20
        elif trace.status == RuleSeverity.WARNING:
            score -= 5
            
    return max(0, min(100, score))

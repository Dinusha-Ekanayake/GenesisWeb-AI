from langgraph.graph import StateGraph, END
from .state import ProjectState
from .nodes.project_manager import project_manager_node
from .nodes.requirement_analysis import requirement_analysis_node
from .nodes.genesis_compiler import genesis_compiler_node
from .nodes.genesis_generator import genesis_generator_node
from langgraph.checkpoint.sqlite import SqliteSaver

memory = SqliteSaver.from_conn_string(":memory:")

workflow = StateGraph(ProjectState)

workflow.add_node("ProjectManager", project_manager_node)
workflow.add_node("RequirementAnalyzer", requirement_analysis_node)
workflow.add_node("GenesisCompiler", genesis_compiler_node)
workflow.add_node("GenesisGenerator", genesis_generator_node)

workflow.set_entry_point("ProjectManager")

def route_from_pm(state: ProjectState):
    events = state.get("events", [])
    
    if "ProjectStarted" in events and "RequirementCompleted" not in events:
        return "RequirementAnalyzer"
    elif "RequirementCompleted" in events and "ValidationPassed" not in events and "ValidationFailed" not in events and "ValidationWarning" not in events:
        return "GenesisCompiler"
    elif "ValidationFailed" in events:
        return END # Strict mode halt
    elif ("ValidationPassed" in events or "ApprovalGranted" in events) and "GenerationCompleted" not in events:
        return "GenesisGenerator"
    elif "GenerationCompleted" in events:
        return END
        
    return END

workflow.add_conditional_edges(
    "ProjectManager",
    route_from_pm,
    {
        "RequirementAnalyzer": "RequirementAnalyzer",
        "GenesisCompiler": "GenesisCompiler",
        "GenesisGenerator": "GenesisGenerator",
        END: END
    }
)

workflow.add_edge("RequirementAnalyzer", "ProjectManager")
workflow.add_edge("GenesisCompiler", "ProjectManager")
workflow.add_edge("GenesisGenerator", "ProjectManager")

app = workflow.compile(
    checkpointer=memory,
    interrupt_before=["GenesisGenerator"] 
)

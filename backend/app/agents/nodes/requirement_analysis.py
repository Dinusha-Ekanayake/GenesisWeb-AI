import json
from pydantic import BaseModel
from ...core.workspace import WorkspaceManager
import sys
import os
# We add the root path to ensure we can import genesis_engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))
from genesis_engine.models.spec import ProjectSpecification
from ..state import ProjectState
from ..llm import get_llm
from langchain_core.prompts import ChatPromptTemplate


def requirement_analysis_node(state: ProjectState) -> dict:
    """
    LangGraph node: Analyzes the user prompt and produces a ProjectSpecification.
    
    This node is production code. It does NOT contain any test hooks, environment
    variable branching, or mocked responses. Tests must use unittest.mock.patch
    to inject a mock LLM via the `get_llm` function.
    """
    prompt = state.get("user_prompt", "")
    project_id = state.get("project_id", "")

    llm = get_llm()
    structured_llm = llm.with_structured_output(ProjectSpecification)

    system_prompt = """
    You are an expert Software Requirements Analyst.
    Your sole job is to interpret the user's prompt and output a comprehensive ProjectSpecification JSON.
    This JSON will be the single source of truth for the entire downstream development team.
    Identify the required pages, core components, authentication needs, and UI theme.
    """

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{user_prompt}")
    ])

    try:
        result: ProjectSpecification = (chat_prompt | structured_llm).invoke({"user_prompt": prompt})
        spec_dict = result.model_dump()

        # Return the specification domain result.
        # Disk persistence is handled by the orchestrating controller/node outside this domain node.
        artifact_path = None
        if project_id:
            project_dir = WorkspaceManager.get_project_dir(project_id)
            spec_path = project_dir / "specification" / "requirements.json"
            artifact_path = str(spec_path)

        return {
            "specification": spec_dict,
            "events": ["RequirementCompleted"],
            "artifacts": {"requirements.json": artifact_path} if artifact_path else {},
            "status": "ANALYSIS_COMPLETE",
            "_persist_spec": {"path": artifact_path, "data": spec_dict} if artifact_path else None,
        }
    except Exception as e:
        return {"errors": [f"RequirementAnalyzer failed: {str(e)}"]}

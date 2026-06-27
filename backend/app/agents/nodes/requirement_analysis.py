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
    prompt = state.get("user_prompt", "")
    project_id = state.get("project_id", "")
    print(f"[RequirementAnalyzer] Analyzing prompt for Project {project_id}...")
    
    if os.environ.get("MOCK_LLM_FOR_TEST") == "1":
        print("[RequirementAnalyzer] MOCK_LLM_FOR_TEST is set. Bypassing OpenAI API...")
        result = ProjectSpecification(
            project_id=project_id,
            name="Mocked CRM",
            description="A simple CRM dashboard",
            pages=["Dashboard", "Settings"],
            components=["Sidebar", "NavigationBar"]
        )
    else:
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
        # Generate the specification
        if os.environ.get("MOCK_LLM_FOR_TEST") != "1":
            result: ProjectSpecification = (chat_prompt | structured_llm).invoke({"user_prompt": prompt})
            
        spec_dict = result.model_dump()
        
        # Write artifact to the physical workspace
        if project_id:
            project_dir = WorkspaceManager.get_project_dir(project_id)
            spec_path = project_dir / "specification" / "requirements.json"
            
            with open(spec_path, "w") as f:
                json.dump(spec_dict, f, indent=4)
                
            artifact_entry = {"requirements.json": str(spec_path)}
        else:
            artifact_entry = {}
            
        return {
            "specification": spec_dict,
            "events": ["RequirementCompleted"],
            "artifacts": artifact_entry,
            "status": "ANALYSIS_COMPLETE"
        }
    except Exception as e:
        return {"errors": [f"RequirementAnalyzer failed: {str(e)}"]}

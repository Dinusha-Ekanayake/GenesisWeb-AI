import ast
from ..state import ProjectState
from ..llm import get_llm
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List

class TestResult(BaseModel):
    passed: bool = Field(description="True if the code passes tests/linting, False otherwise")
    issues: List[str] = Field(description="List of detected bugs, syntax errors, or improvements")

def testing_agent_node(state: ProjectState) -> dict:
    """
    The Testing Agent performs static analysis and unit test generation.
    It checks for syntax errors, missing imports, and logic flaws.
    """
    print("[TestingAgent] Validating generated code...")
    
    generated_backend = state.get("generated_backend", {})
    errors = []
    
    # 1. Quick Python Syntax Check (No LLM needed, saves tokens and time)
    for filename, content in generated_backend.items():
        if filename.endswith('.py'):
            try:
                ast.parse(content)
            except SyntaxError as e:
                errors.append(f"SyntaxError in {filename}: {e.msg} at line {e.lineno}")
    
    if errors:
        return {"errors": errors, "status": "TEST_FAILED"}
        
    # 2. LLM-based Logic Review
    llm = get_llm()
    structured_llm = llm.with_structured_output(TestResult)
    
    system_prompt = """
    You are an expert Python QA Engineer.
    Review the provided generated code files for security flaws, missing imports, or runtime bugs.
    If you find issues, list them. If it looks solid, set passed=True.
    """
    
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Generated Code: {code}")
    ])
    
    try:
        result: TestResult = (chat_prompt | structured_llm).invoke({"code": generated_backend})
        if not result.passed:
            return {"errors": result.issues, "status": "TEST_FAILED"}
            
        return {"status": "TEST_PASSED"}
    except Exception as e:
        return {"errors": [f"TestingAgent failed: {str(e)}"]}

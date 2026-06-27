from typing import List, Dict
from ..interfaces.plugin import GenerationPlugin
from ..models.outputs import GenerationPlan, FileArtifact
from ..rules.base import RuleContext
from ..utils.workspace_adapter import WorkspaceAdapter

class GenerationEngine:
    def __init__(self, workspace_root: str):
        self.workspace_adapter = WorkspaceAdapter(workspace_root)
        self.plugins: Dict[str, GenerationPlugin] = {}
        
    def register_plugin(self, plugin: GenerationPlugin):
        self.plugins[plugin.name] = plugin
        
    def execute(self, plan: GenerationPlan, context: RuleContext, project_id: str) -> None:
        all_artifacts = []
        
        steps = sorted(plan.steps, key=lambda s: s.execution_priority)
        
        for step in steps:
            plugin = self.plugins.get(step.target_plugin)
            if plugin:
                artifacts = plugin.generate(context)
                all_artifacts.extend(artifacts)
                
        self.workspace_adapter.write_code_artifacts(project_id, all_artifacts)

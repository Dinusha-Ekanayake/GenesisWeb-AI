from ...models.ir import GenesisIR
from ...models.graphs import PageGraph, ComponentGraph, ComponentNode, GraphNodeMetadata
from ...models.outputs import ArchitectureDecisionRecord, ArchitectureDecision

class ComponentPlanner:
    def plan(self, page_graph: PageGraph, ir: GenesisIR, adr: ArchitectureDecisionRecord) -> ComponentGraph:
        components = []
        
        # Add a global layout component deterministically
        layout_id = "component.dashboard_layout"
        components.append(ComponentNode(
            id=layout_id,
            name="DashboardLayout",
            props={"children": "ReactNode"},
            state={},
            children=[],
            metadata=GraphNodeMetadata(created_by="ComponentPlanner", derived_from=["Global"])
        ))
        
        adr.decisions.append(ArchitectureDecision(
            decision="Added DashboardLayout",
            reason="Standardized app layout container",
            source="ComponentPlanner Base Rule",
            affected_graphs=["ComponentGraph"]
        ))
        
        # Macro components per page
        for page in page_graph.pages:
            macro_id = f"component.{page.id.replace('page.', '')}_view"

            components.append(ComponentNode(
                id=macro_id,
                name=f"{page.name.replace(' ', '')}View",
                props={},
                state={"isLoading": "boolean"},
                children=[],
                metadata=GraphNodeMetadata(
                    created_by="ComponentPlanner",
                    derived_from=[page.id],
                    depends_on=[page.id]
                )
            ))

            adr.decisions.append(ArchitectureDecision(
                decision=f"Added macro component {macro_id}",
                reason=f"Primary view container for {page.route}",
                source=page.id,
                affected_graphs=["ComponentGraph"]
            ))

        # Spec-declared reusable components (distinct from page macro views)
        for comp_name in ir.components:
            comp_id = f"component.spec.{comp_name.lower()}"
            components.append(ComponentNode(
                id=comp_id,
                name=comp_name,
                props={},
                state={},
                children=[],
                metadata=GraphNodeMetadata(
                    created_by="SpecComponent",
                    derived_from=["ProjectSpecification.components"],
                    depends_on=[]
                )
            ))
            adr.decisions.append(ArchitectureDecision(
                decision=f"Added spec-declared component {comp_name}",
                reason="Explicitly declared in spec.components; generated as a reusable module",
                source="ProjectSpecification",
                affected_graphs=["ComponentGraph"]
            ))

        return ComponentGraph(components=components)

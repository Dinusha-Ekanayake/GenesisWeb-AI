from ...models.ir import GenesisIR
from ...models.graphs import DatabaseGraph, DatabaseTableNode, GraphNodeMetadata
from ...models.outputs import ArchitectureDecisionRecord, ArchitectureDecision

class DatabasePlanner:
    def plan(self, ir: GenesisIR, adr: ArchitectureDecisionRecord) -> DatabaseGraph:
        tables = []
        
        # Deterministically parse entities into tables
        for entity in ir.entities:
            node_id = f"database.{entity.name.lower()}"
            
            tables.append(DatabaseTableNode(
                id=node_id,
                name=entity.name,
                columns=entity.attributes,
                relations=entity.relations,
                primary_key="id",
                metadata=GraphNodeMetadata(
                    created_by="DatabasePlanner",
                    derived_from=["GenesisIR.entities"]
                )
            ))
            
            adr.decisions.append(ArchitectureDecision(
                decision=f"Created database table {entity.name}",
                reason="Entity mapping",
                source="GenesisIR",
                affected_graphs=["DatabaseGraph"]
            ))
            
        return DatabaseGraph(tables=tables)

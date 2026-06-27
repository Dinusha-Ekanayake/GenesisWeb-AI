from ...models.ir import GenesisIR
from ...models.graphs import FeatureGraph, FeatureNode, GraphNodeMetadata
from ...models.outputs import ArchitectureDecisionRecord, ArchitectureDecision

class FeaturePlanner:
    def plan(self, ir: GenesisIR, adr: ArchitectureDecisionRecord) -> FeatureGraph:
        features = []
        for feat in ir.features:
            node_id = f"feature.{feat.lower().replace(' ', '_')}"
            
            # Traceability Metadata
            metadata = GraphNodeMetadata(
                created_by="FeaturePlanner",
                derived_from=["GenesisIR.features"],
                depends_on=[]
            )
            
            features.append(FeatureNode(
                id=node_id,
                name=feat,
                requirements=[f"Implement {feat}"],
                metadata=metadata
            ))
            
            # Architecture Decision Record
            adr.decisions.append(ArchitectureDecision(
                decision=f"Included feature {feat}",
                reason="Explicitly requested in IR",
                source="GenesisIR",
                affected_graphs=["FeatureGraph"]
            ))
            
        return FeatureGraph(features=features)

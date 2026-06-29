import { RunRouteScaffold } from "@/components/routes/RunRouteScaffold";

export default function RunArchitecturePage({ params }: { params: { id: string; runId: string } }) {
  return <RunRouteScaffold projectId={params.id} runId={params.runId} surface="architecture" />;
}

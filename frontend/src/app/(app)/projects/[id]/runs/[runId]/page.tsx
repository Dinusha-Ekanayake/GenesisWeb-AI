import { RunRouteScaffold } from "@/components/routes/RunRouteScaffold";

export default function RunOverviewPage({ params }: { params: { id: string; runId: string } }) {
  return <RunRouteScaffold projectId={params.id} runId={params.runId} surface="overview" />;
}

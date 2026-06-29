import { LimitedState, RouteScaffold } from "@/components/routes/RouteScaffold";

export default function CompilerPage() {
  return (
    <RouteScaffold
      eyebrow="Compiler"
      title="Compiler"
      description="Target compiler route shell. The existing dashboard compiler remains the working implementation for now."
    >
      <LimitedState title="Compiler experience deferred" description="No new compiler UI or backend endpoints are implemented in Milestone 3." />
    </RouteScaffold>
  );
}

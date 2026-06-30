import { LimitedState, RouteScaffold } from "@/components/routes/RouteScaffold";

export default function TeamPage() {
  return (
    <RouteScaffold eyebrow="Organization" title="Team" description="Team route shell for future organization membership and roles.">
      <LimitedState title="Team management deferred" description="No team backend contract is available." />
    </RouteScaffold>
  );
}

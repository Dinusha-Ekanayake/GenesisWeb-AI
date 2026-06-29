import { LimitedState, RouteScaffold } from "@/components/routes/RouteScaffold";

export default function SettingsPage() {
  return (
    <RouteScaffold eyebrow="Organization" title="Settings" description="Settings route shell for future organization and project configuration.">
      <LimitedState title="Settings deferred" description="No settings backend contract is introduced in Milestone 3." />
    </RouteScaffold>
  );
}

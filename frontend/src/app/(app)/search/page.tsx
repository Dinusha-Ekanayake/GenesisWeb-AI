import { LimitedState, RouteScaffold } from "@/components/routes/RouteScaffold";

export default function SearchPage() {
  return (
    <RouteScaffold eyebrow="Search" title="Search" description="Search route shell for future specification, Run, and artifact discovery.">
      <LimitedState title="Search deferred" description="No search backend endpoint exists yet, so this page intentionally avoids fake results." />
    </RouteScaffold>
  );
}

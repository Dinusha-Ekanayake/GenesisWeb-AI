import { RouteScaffold } from "@/components/routes/RouteScaffold";
import { AppearanceCard } from "./AppearanceCard";
import { ShellPreferencesCard } from "./ShellPreferencesCard";
import { ShortcutReferenceCard } from "./ShortcutReferenceCard";

export function SettingsPage() {
  return (
    <RouteScaffold
      eyebrow="Preferences"
      title="Settings"
      description="Local preferences for the Genesis Engine interface."
    >
      <div className="max-w-2xl space-y-6">
        <p className="text-xs text-[color:var(--text-tertiary)]">
          Settings are stored locally in this browser and device. They are not synced to any backend.
        </p>
        <AppearanceCard />
        <ShellPreferencesCard />
        <ShortcutReferenceCard />
      </div>
    </RouteScaffold>
  );
}

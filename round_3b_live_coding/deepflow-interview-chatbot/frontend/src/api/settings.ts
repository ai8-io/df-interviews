export interface AppSettings {
  system_prompt: string;
  default_model: string;
  reasoning_enabled: boolean;
  max_context_tokens: number;
  updated_at: string | null;
}

export interface AppSettingsUpdate {
  system_prompt?: string;
  default_model?: string;
  reasoning_enabled?: boolean;
  max_context_tokens?: number;
}

export async function fetchSettings(): Promise<AppSettings> {
  const res = await fetch("/api/settings");
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  return res.json();
}

export async function updateSettings(
  update: AppSettingsUpdate,
): Promise<AppSettings> {
  const res = await fetch("/api/settings", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(update),
  });
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  return res.json();
}

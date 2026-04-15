import { useEffect, useState } from "react";
import { AVAILABLE_MODELS } from "@interview/contracts";
import {
  fetchSettings,
  updateSettings,
  type AppSettings,
} from "../api/settings";

export default function Settings() {
  const [settings, setSettings] = useState<AppSettings | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  const [systemPrompt, setSystemPrompt] = useState("");
  const [defaultModel, setDefaultModel] = useState("");
  const [reasoningEnabled, setReasoningEnabled] = useState(true);
  const [maxContextTokens, setMaxContextTokens] = useState(100000);

  useEffect(() => {
    fetchSettings()
      .then((s) => {
        setSettings(s);
        setSystemPrompt(s.system_prompt);
        setDefaultModel(s.default_model);
        setReasoningEnabled(s.reasoning_enabled);
        setMaxContextTokens(s.max_context_tokens);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const handleSave = async () => {
    setSaving(true);
    setSaved(false);
    try {
      const updated = await updateSettings({
        system_prompt: systemPrompt,
        default_model: defaultModel,
        reasoning_enabled: reasoningEnabled,
        max_context_tokens: maxContextTokens,
      });
      setSettings(updated);
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch {
      alert("Failed to save settings");
    } finally {
      setSaving(false);
    }
  };

  const hasChanges =
    settings &&
    (systemPrompt !== settings.system_prompt ||
      defaultModel !== settings.default_model ||
      reasoningEnabled !== settings.reasoning_enabled ||
      maxContextTokens !== settings.max_context_tokens);

  if (loading) {
    return (
      <div className="flex flex-1 items-center justify-center bg-gray-50">
        <p className="text-gray-400">Loading settings...</p>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto bg-gray-50">
      <div className="mx-auto max-w-2xl px-8 py-8">
        <div className="mb-6">
          <h1 className="text-xl font-semibold text-gray-900">Settings</h1>
          <p className="mt-1 text-sm text-gray-500">
            Configure the HR assistant behaviour and model settings
          </p>
        </div>

        <div className="space-y-6 rounded-xl border border-gray-200 bg-white p-6">
          <div>
            <label className="mb-1.5 block text-sm font-medium text-gray-700">
              System Prompt
            </label>
            <textarea
              value={systemPrompt}
              onChange={(e) => setSystemPrompt(e.target.value)}
              rows={6}
              className="w-full rounded-lg border border-gray-200 bg-gray-50 px-3 py-2 text-sm text-gray-900 outline-none transition-colors focus:border-blue-300 focus:bg-white focus:ring-2 focus:ring-blue-100"
            />
            <p className="mt-1 text-xs text-gray-400">
              Instructions given to the model at the start of every conversation
            </p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="mb-1.5 block text-sm font-medium text-gray-700">
                Default Model
              </label>
              <select
                value={defaultModel}
                onChange={(e) => setDefaultModel(e.target.value)}
                className="w-full rounded-lg border border-gray-200 bg-gray-50 px-3 py-2 text-sm text-gray-700 outline-none focus:border-blue-300 focus:ring-2 focus:ring-blue-100"
              >
                {AVAILABLE_MODELS.map((m) => (
                  <option key={m} value={m}>
                    {m.split("/").pop()?.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="mb-1.5 block text-sm font-medium text-gray-700">
                Max Context Tokens
              </label>
              <input
                type="number"
                value={maxContextTokens}
                onChange={(e) => setMaxContextTokens(Number(e.target.value))}
                min={1000}
                max={500000}
                step={1000}
                className="w-full rounded-lg border border-gray-200 bg-gray-50 px-3 py-2 text-sm text-gray-900 outline-none focus:border-blue-300 focus:ring-2 focus:ring-blue-100"
              />
            </div>
          </div>

          <div className="flex items-center justify-between rounded-lg border border-gray-100 bg-gray-50 px-4 py-3">
            <div>
              <p className="text-sm font-medium text-gray-700">
                Enable Reasoning
              </p>
              <p className="text-xs text-gray-400">
                Let the model think step-by-step before responding (higher
                quality, slower)
              </p>
            </div>
            <button
              onClick={() => setReasoningEnabled(!reasoningEnabled)}
              className={`relative h-6 w-11 rounded-full transition-colors ${
                reasoningEnabled ? "bg-blue-600" : "bg-gray-300"
              }`}
            >
              <span
                className={`absolute left-0.5 top-0.5 h-5 w-5 rounded-full bg-white shadow transition-transform ${
                  reasoningEnabled ? "translate-x-5" : "translate-x-0"
                }`}
              />
            </button>
          </div>

          <div className="flex items-center justify-between border-t border-gray-100 pt-4">
            {settings?.updated_at && (
              <p className="text-xs text-gray-400">
                Last updated:{" "}
                {new Date(settings.updated_at).toLocaleString("en-GB")}
              </p>
            )}
            <div className="flex items-center gap-3">
              {saved && (
                <span className="text-sm text-green-600">Saved!</span>
              )}
              <button
                onClick={handleSave}
                disabled={saving || !hasChanges}
                className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-500 disabled:opacity-40"
              >
                {saving ? "Saving..." : "Save Changes"}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

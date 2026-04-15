export interface AnalyticsOverview {
  total_conversations: number;
  total_messages: number;
  avg_messages_per_conversation: number;
  total_user_messages: number;
  total_assistant_messages: number;
}

export interface ResponseTimeStats {
  avg_response_ms: number;
  p50_response_ms: number;
  p95_response_ms: number;
  slowest_response_ms: number;
  total_measured: number;
}

export interface ModelUsageEntry {
  model: string;
  message_count: number;
  avg_response_ms: number | null;
}

export interface ModelUsageStats {
  entries: ModelUsageEntry[];
  total_messages_with_model: number;
}

export interface DailyMessageCount {
  date: string;
  count: number;
}

export interface ConversationActivity {
  daily_messages: DailyMessageCount[];
  busiest_day: string | null;
  total_days_active: number;
}

export async function fetchOverview(): Promise<AnalyticsOverview> {
  const res = await fetch("/api/analytics/overview");
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  return res.json();
}

export async function fetchResponseTimes(): Promise<ResponseTimeStats> {
  const res = await fetch("/api/analytics/response-times");
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  return res.json();
}

export async function fetchModelUsage(): Promise<ModelUsageStats> {
  const res = await fetch("/api/analytics/model-usage");
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  return res.json();
}

export async function fetchActivity(): Promise<ConversationActivity> {
  const res = await fetch("/api/analytics/activity");
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  return res.json();
}

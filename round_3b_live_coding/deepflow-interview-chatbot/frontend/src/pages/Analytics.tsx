import { useEffect, useState } from "react";
import {
  fetchOverview,
  fetchResponseTimes,
  fetchModelUsage,
  fetchActivity,
  type AnalyticsOverview,
  type ResponseTimeStats,
  type ModelUsageStats,
  type ConversationActivity,
} from "../api/analytics";

export default function Analytics() {
  const [overview, setOverview] = useState<AnalyticsOverview | null>(null);
  const [responseTimes, setResponseTimes] = useState<ResponseTimeStats | null>(null);
  const [modelUsage, setModelUsage] = useState<ModelUsageStats | null>(null);
  const [activity, setActivity] = useState<ConversationActivity | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetchOverview(),
      fetchResponseTimes(),
      fetchModelUsage(),
      fetchActivity(),
    ])
      .then(([o, r, m, a]) => {
        setOverview(o);
        setResponseTimes(r);
        setModelUsage(m);
        setActivity(a);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex flex-1 items-center justify-center bg-gray-50">
        <p className="text-gray-400">Loading analytics...</p>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto bg-gray-50">
      <div className="mx-auto max-w-6xl px-8 py-8">
        <div className="mb-6">
          <h1 className="text-xl font-semibold text-gray-900">Analytics</h1>
          <p className="mt-1 text-sm text-gray-500">
            Usage metrics and performance data for the HR chatbot
          </p>
        </div>

        {overview && (
          <div className="mb-8 grid grid-cols-2 gap-4 lg:grid-cols-5">
            <StatCard label="Conversations" value={overview.total_conversations} />
            <StatCard label="Total Messages" value={overview.total_messages} />
            <StatCard
              label="Avg per Convo"
              value={overview.avg_messages_per_conversation}
              decimal
            />
            <StatCard label="User Messages" value={overview.total_user_messages} />
            <StatCard label="AI Responses" value={overview.total_assistant_messages} />
          </div>
        )}

        <div className="mb-8 grid grid-cols-1 gap-6 lg:grid-cols-2">
          {responseTimes && (
            <div className="rounded-xl border border-gray-200 bg-white p-6">
              <h2 className="mb-4 text-sm font-semibold text-gray-900">
                Response Times
              </h2>
              {responseTimes.total_measured === 0 ? (
                <p className="text-sm text-gray-400">No response time data yet</p>
              ) : (
                <div className="space-y-3">
                  <MetricRow label="Average" value={formatMs(responseTimes.avg_response_ms)} />
                  <MetricRow label="Median (p50)" value={formatMs(responseTimes.p50_response_ms)} />
                  <MetricRow label="p95" value={formatMs(responseTimes.p95_response_ms)} />
                  <MetricRow label="Slowest" value={formatMs(responseTimes.slowest_response_ms)} />
                  <div className="border-t border-gray-100 pt-2">
                    <MetricRow
                      label="Measured responses"
                      value={responseTimes.total_measured.toString()}
                    />
                  </div>
                </div>
              )}
            </div>
          )}

          {modelUsage && (
            <div className="rounded-xl border border-gray-200 bg-white p-6">
              <h2 className="mb-4 text-sm font-semibold text-gray-900">
                Model Usage
              </h2>
              {modelUsage.entries.length === 0 ? (
                <p className="text-sm text-gray-400">No model usage data yet</p>
              ) : (
                <div className="space-y-3">
                  {modelUsage.entries.map((entry) => {
                    const pct =
                      modelUsage.total_messages_with_model > 0
                        ? Math.round(
                            (entry.message_count /
                              modelUsage.total_messages_with_model) *
                              100,
                          )
                        : 0;
                    return (
                      <div key={entry.model}>
                        <div className="flex items-center justify-between text-sm">
                          <span className="font-medium text-gray-700">
                            {entry.model.split("/").pop()}
                          </span>
                          <span className="text-gray-500">
                            {entry.message_count} msgs ({pct}%)
                          </span>
                        </div>
                        <div className="mt-1 h-2 rounded-full bg-gray-100">
                          <div
                            className="h-2 rounded-full bg-blue-500"
                            style={{ width: `${pct}%` }}
                          />
                        </div>
                        {entry.avg_response_ms && (
                          <p className="mt-0.5 text-xs text-gray-400">
                            avg {formatMs(entry.avg_response_ms)}
                          </p>
                        )}
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          )}
        </div>

        {activity && activity.daily_messages.length > 0 && (
          <div className="rounded-xl border border-gray-200 bg-white p-6">
            <h2 className="mb-4 text-sm font-semibold text-gray-900">
              Daily Activity
            </h2>
            <div className="flex items-end gap-1" style={{ height: 120 }}>
              {activity.daily_messages.map((d) => {
                const maxCount = Math.max(
                  ...activity.daily_messages.map((x) => x.count),
                );
                const height = maxCount > 0 ? (d.count / maxCount) * 100 : 0;
                return (
                  <div
                    key={d.date}
                    className="group relative flex-1"
                    title={`${d.date}: ${d.count} messages`}
                  >
                    <div
                      className="w-full rounded-t bg-blue-500 transition-colors group-hover:bg-blue-600"
                      style={{ height: `${height}%`, minHeight: d.count > 0 ? 4 : 0 }}
                    />
                  </div>
                );
              })}
            </div>
            <div className="mt-2 flex justify-between text-xs text-gray-400">
              <span>{activity.daily_messages[0]?.date}</span>
              <span>
                {activity.daily_messages[activity.daily_messages.length - 1]?.date}
              </span>
            </div>
            {activity.busiest_day && (
              <p className="mt-2 text-xs text-gray-500">
                Busiest day: {activity.busiest_day} &middot;{" "}
                {activity.total_days_active} days active
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function StatCard({
  label,
  value,
  decimal,
}: {
  label: string;
  value: number;
  decimal?: boolean;
}) {
  return (
    <div className="rounded-xl border border-gray-200 bg-white p-4">
      <p className="text-xs font-medium uppercase tracking-wide text-gray-500">
        {label}
      </p>
      <p className="mt-1 text-2xl font-semibold text-gray-900">
        {decimal ? value.toFixed(1) : value}
      </p>
    </div>
  );
}

function MetricRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between text-sm">
      <span className="text-gray-600">{label}</span>
      <span className="font-medium text-gray-900">{value}</span>
    </div>
  );
}

function formatMs(ms: number): string {
  if (ms < 1000) return `${Math.round(ms)}ms`;
  return `${(ms / 1000).toFixed(1)}s`;
}

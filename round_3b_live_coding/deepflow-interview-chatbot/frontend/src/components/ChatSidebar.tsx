import type { ConversationSummary } from "../api/chat";

interface Props {
  conversations: ConversationSummary[];
  activeId: string | undefined;
  onSelect: (id: string) => void;
  onNew: () => void;
}

function formatDate(iso: string | null): string {
  if (!iso) return "";
  const d = new Date(iso);
  const now = new Date();
  const diff = now.getTime() - d.getTime();
  if (diff < 86_400_000) return "Today";
  if (diff < 172_800_000) return "Yesterday";
  return d.toLocaleDateString("en-GB", { day: "numeric", month: "short" });
}

export default function ChatSidebar({
  conversations,
  activeId,
  onSelect,
  onNew,
}: Props) {
  return (
    <div className="flex w-64 shrink-0 flex-col border-r border-gray-200 bg-white">
      <div className="border-b border-gray-200 px-3 py-3">
        <button
          onClick={onNew}
          className="flex w-full items-center gap-2 rounded-lg border border-gray-200 bg-gray-50 px-3 py-2 text-sm text-gray-600 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:text-gray-900"
        >
          <svg
            className="h-4 w-4"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 4.5v15m7.5-7.5h-15"
            />
          </svg>
          New conversation
        </button>
      </div>

      <div className="flex-1 overflow-y-auto px-2 py-1">
        {conversations.length === 0 && (
          <p className="px-3 py-8 text-center text-xs text-gray-400">
            No conversations yet
          </p>
        )}
        {conversations.map((c) => (
          <button
            key={c.id}
            onClick={() => onSelect(c.id)}
            className={`mb-0.5 w-full rounded-lg px-3 py-2.5 text-left transition-colors ${
              c.id === activeId
                ? "bg-blue-50 text-gray-900"
                : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
            }`}
          >
            <span className="block truncate text-sm">
              {c.title || "Untitled conversation"}
            </span>
            <span className="mt-0.5 block text-xs text-gray-400">
              {formatDate(c.created_at)}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}

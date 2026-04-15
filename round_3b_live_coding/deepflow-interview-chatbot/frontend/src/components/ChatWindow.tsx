import { AVAILABLE_MODELS } from "@interview/contracts";
import type { Message } from "../hooks/useChat";
import MessageList from "./MessageList";
import MessageInput from "./MessageInput";

interface Props {
  messages: Message[];
  isLoading: boolean;
  onSend: (content: string) => void;
  model: string;
  onModelChange: (model: string) => void;
}

function displayName(model: string): string {
  const last = model.split("/").pop() ?? model;
  return last
    .replace(/-/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

export default function ChatWindow({
  messages,
  isLoading,
  onSend,
  model,
  onModelChange,
}: Props) {
  return (
    <div className="flex flex-1 flex-col bg-gray-50">
      <div className="flex items-center justify-between border-b border-gray-200 bg-white px-8 py-4">
        <div>
          <h1 className="text-base font-semibold text-gray-900">
            HR Assistant
          </h1>
          <p className="text-xs text-gray-500">
            Ask about employees, compensation, and team structure
          </p>
        </div>
        <div className="flex items-center gap-2">
          <label className="text-xs text-gray-500">Model</label>
          <select
            value={model}
            onChange={(e) => onModelChange(e.target.value)}
            className="rounded-lg border border-gray-200 bg-gray-50 px-3 py-1.5 text-xs text-gray-700 outline-none transition-colors hover:border-gray-300 focus:border-blue-300 focus:ring-2 focus:ring-blue-100"
          >
            {AVAILABLE_MODELS.map((m) => (
              <option key={m} value={m}>
                {displayName(m)}
              </option>
            ))}
          </select>
        </div>
      </div>

      <MessageList messages={messages} isLoading={isLoading} />
      <MessageInput onSend={onSend} disabled={isLoading} />
    </div>
  );
}

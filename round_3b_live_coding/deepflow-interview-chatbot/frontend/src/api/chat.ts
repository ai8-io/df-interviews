import type { SendMessageResponseType } from "@interview/contracts";

export interface ConversationSummary {
  id: string;
  title: string | null;
  created_at: string | null;
}

export interface PersistedMessage {
  id: string;
  conversation_id: string;
  role: "user" | "assistant";
  content: string;
  thinking_content: string | null;
  created_at: string | null;
}

export async function sendMessage(
  message: string,
  conversationId?: string,
  model?: string,
): Promise<SendMessageResponseType> {
  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message,
      conversation_id: conversationId ?? null,
      model: model ?? undefined,
    }),
  });
  if (!res.ok) throw new Error(`Chat request failed: ${res.status}`);
  return res.json();
}

export async function fetchConversations(): Promise<ConversationSummary[]> {
  const res = await fetch("/api/conversations");
  if (!res.ok) throw new Error(`Failed to fetch conversations: ${res.status}`);
  return res.json();
}

export async function fetchMessages(
  conversationId: string,
): Promise<PersistedMessage[]> {
  const res = await fetch(`/api/conversations/${conversationId}/messages`);
  if (!res.ok) throw new Error(`Failed to fetch messages: ${res.status}`);
  return res.json();
}

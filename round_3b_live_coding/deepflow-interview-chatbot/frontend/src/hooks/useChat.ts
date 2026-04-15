import { useCallback, useEffect, useState } from "react";
import { DEFAULT_MODEL } from "@interview/contracts";
import {
  sendMessage,
  fetchMessages,
  fetchConversations,
  type ConversationSummary,
} from "../api/chat";

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | undefined>();
  const [conversations, setConversations] = useState<ConversationSummary[]>([]);
  const [model, setModel] = useState<string>(DEFAULT_MODEL);

  const refreshConversations = useCallback(async () => {
    try {
      const list = await fetchConversations();
      setConversations(list);
    } catch {
      /* non-critical */
    }
  }, []);

  useEffect(() => {
    refreshConversations();
  }, [refreshConversations]);

  const loadConversation = useCallback(async (id: string) => {
    setConversationId(id);
    setIsLoading(true);
    try {
      const msgs = await fetchMessages(id);
      setMessages(
        msgs.map((m) => ({ id: m.id, role: m.role, content: m.content })),
      );
    } catch {
      setMessages([]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const newConversation = useCallback(() => {
    setConversationId(undefined);
    setMessages([]);
  }, []);

  const send = useCallback(
    async (content: string) => {
      const userMsg: Message = {
        id: crypto.randomUUID(),
        role: "user",
        content,
      };
      setMessages((prev) => [...prev, userMsg]);
      setIsLoading(true);

      try {
        const data = await sendMessage(content, conversationId, model);
        setConversationId(data.conversation_id);

        const assistantMsg: Message = {
          id: data.message_id,
          role: "assistant",
          content: data.content,
        };
        setMessages((prev) => [...prev, assistantMsg]);
        refreshConversations();
      } catch {
        setMessages((prev) => [
          ...prev,
          {
            id: crypto.randomUUID(),
            role: "assistant",
            content: "Something went wrong. Please try again.",
          },
        ]);
      } finally {
        setIsLoading(false);
      }
    },
    [conversationId, model, refreshConversations],
  );

  return {
    messages,
    isLoading,
    conversationId,
    conversations,
    model,
    setModel,
    send,
    loadConversation,
    newConversation,
  };
}

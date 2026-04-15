import { useChat } from "../hooks/useChat";
import ChatWindow from "../components/ChatWindow";
import ChatSidebar from "../components/ChatSidebar";

export default function ChatPage() {
  const {
    messages,
    isLoading,
    conversationId,
    conversations,
    model,
    setModel,
    send,
    loadConversation,
    newConversation,
  } = useChat();

  return (
    <>
      <ChatSidebar
        conversations={conversations}
        activeId={conversationId}
        onSelect={loadConversation}
        onNew={newConversation}
      />
      <ChatWindow
        messages={messages}
        isLoading={isLoading}
        onSend={send}
        model={model}
        onModelChange={setModel}
      />
    </>
  );
}

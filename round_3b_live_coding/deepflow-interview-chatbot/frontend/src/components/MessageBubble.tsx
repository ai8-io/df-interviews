import ReactMarkdown from "react-markdown";
import type { Message } from "../hooks/useChat";

interface Props {
  message: Message;
}

export default function MessageBubble({ message }: Props) {
  const isUser = message.role === "user";

  if (isUser) {
    return (
      <div className="flex justify-end">
        <div className="max-w-[75%] rounded-2xl rounded-br-md bg-blue-600 px-4 py-2.5 shadow-sm">
          <p className="whitespace-pre-wrap text-sm leading-relaxed text-white">
            {message.content}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex justify-start">
      <div className="prose-chat max-w-[85%] rounded-2xl rounded-bl-md bg-white px-4 py-3 shadow-sm ring-1 ring-gray-200">
        <ReactMarkdown>{message.content}</ReactMarkdown>
      </div>
    </div>
  );
}

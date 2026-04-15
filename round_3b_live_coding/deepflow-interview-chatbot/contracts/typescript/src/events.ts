import { z } from "zod";

export const MessageCreatedEventData = z.object({
  conversation_id: z.string(),
  message_id: z.string(),
  role: z.string(),
  message_count: z.number().int(),
});
export type MessageCreatedEventData = z.infer<typeof MessageCreatedEventData>;

export const MessageCreatedEvent = z.object({
  name: z.literal("chat/message.created"),
  data: MessageCreatedEventData,
});
export type MessageCreatedEvent = z.infer<typeof MessageCreatedEvent>;

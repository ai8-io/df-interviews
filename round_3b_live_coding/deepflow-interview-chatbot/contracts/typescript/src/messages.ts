import { z } from "zod";

export const Role = z.enum(["user", "assistant"]);
export type Role = z.infer<typeof Role>;

export const ChatMessage = z.object({
  id: z.string().uuid(),
  conversation_id: z.string(),
  role: Role,
  content: z.string(),
  thinking_content: z.string().nullable().optional(),
  created_at: z.string().datetime(),
});
export type ChatMessage = z.infer<typeof ChatMessage>;

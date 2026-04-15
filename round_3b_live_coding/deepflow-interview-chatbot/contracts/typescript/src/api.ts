import { z } from "zod";

export const AVAILABLE_MODELS = [
  "anthropic/claude-4.6-opus",
  "openai/gpt-5.4",
  "google/gemini-3.1",
] as const;

export const DEFAULT_MODEL = "anthropic/claude-4.6-opus";

export const SendMessageRequest = z.object({
  message: z.string().min(1),
  conversation_id: z.string().nullable().optional(),
  model: z.string().default(DEFAULT_MODEL),
  reasoning: z.boolean().default(true),
});
export type SendMessageRequest = z.infer<typeof SendMessageRequest>;

export const SendMessageResponse = z.object({
  conversation_id: z.string(),
  message_id: z.string(),
  content: z.string(),
  thinking_content: z.string().nullable().optional(),
});
export type SendMessageResponse = z.infer<typeof SendMessageResponse>;

import { z } from "zod";

export const ChunkType = z.enum(["content", "thinking", "done", "error"]);
export type ChunkType = z.infer<typeof ChunkType>;

export const ThinkingMetadata = z.object({
  content: z.string().default(""),
  is_complete: z.boolean().default(false),
});
export type ThinkingMetadata = z.infer<typeof ThinkingMetadata>;

export const ChatChunk = z.object({
  type: ChunkType,
  content: z.string().default(""),
  thinking: ThinkingMetadata.nullable().optional(),
  conversation_id: z.string().nullable().optional(),
  message_id: z.string().nullable().optional(),
});
export type ChatChunk = z.infer<typeof ChatChunk>;

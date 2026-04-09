import { useRef, useState } from "react";


/**
 * Manages chat state and handles sending messages to the RAG backend.
 *
 * Returns:
 *   messages    — array of { id, role: "user" | "assistant", content, sources? }
 *   isLoading   — true while waiting for a response
 *   errorMessage — non-null if the last request failed
 *   sendMessage — async function to send a new user message
 */
export function useChat() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);
  const nextMessageId = useRef(0);

  async function sendMessage(userText) {
    if (!userText.trim()) return;

    const userMessage = { id: nextMessageId.current++, role: "user", content: userText };
    setMessages((previous) => [...previous, userMessage]);
    setIsLoading(true);
    setErrorMessage(null);

    try {
      const backendUrl = import.meta.env.VITE_API_URL ?? "";
      const response = await fetch(`${backendUrl}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userText }),
      });

      if (!response.ok) {
        setErrorMessage(
          response.status === 503
            ? "The assistant is still loading. Please try again in a moment."
            : "Something went wrong. Please try again."
        );
        return;
      }

      const data = await response.json();

      const assistantMessage = {
        id: nextMessageId.current++,
        role: "assistant",
        content: data.answer,
        sources: data.sources,
      };

      setMessages((previous) => [...previous, assistantMessage]);
    } catch (error) {
      console.error("Chat request failed:", error);
      setErrorMessage("Something went wrong. Please try again.");
    } finally {
      setIsLoading(false);
    }
  }

  return { messages, isLoading, errorMessage, sendMessage };
}

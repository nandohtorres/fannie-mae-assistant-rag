import { useEffect, useRef, useState } from "react";
import {
  Alert,
  Box,
  Chip,
  IconButton,
  InputAdornment,
  TextField,
  Typography,
} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import MessageBubble from "@/components/MessageBubble";
import { useChat } from "@/hooks/useChat";


const SUGGESTED_QUESTIONS = [
  "What are the conforming loan limits?",
  "What credit score is required for a conventional loan?",
  "What are the property eligibility requirements?",
  "How is debt-to-income ratio calculated?",
];


/**
 * Three animated dots shown while the assistant is generating a response.
 * Each dot bounces in sequence to indicate active processing.
 */
function TypingIndicator() {
  return (
    <Box sx={{ display: "flex", justifyContent: "flex-start", mb: 2, pl: 1 }}>
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          gap: 0.6,
          px: 2,
          py: 1.5,
          borderRadius: 2,
          border: "1px solid",
          borderColor: "divider",
          backgroundColor: "background.paper",
        }}
      >
        {[0, 1, 2].map((dotIndex) => (
          <Box
            key={dotIndex}
            sx={{
              width: 7,
              height: 7,
              borderRadius: "50%",
              backgroundColor: "secondary.main",
              animation: "typingBounce 1.2s infinite ease-in-out",
              animationDelay: `${dotIndex * 0.2}s`,
              "@keyframes typingBounce": {
                "0%, 60%, 100%": { transform: "translateY(0)", opacity: 0.5 },
                "30%": { transform: "translateY(-6px)", opacity: 1 },
              },
            }}
          />
        ))}
      </Box>
    </Box>
  );
}


/**
 * The main chat interface. Renders the message history, suggested questions for
 * new sessions, the typing indicator, and the text input field.
 */
export default function ChatWindow() {
  const { messages, isLoading, errorMessage, sendMessage } = useChat();
  const [inputText, setInputText] = useState("");
  const messagesEndRef = useRef(null);

  // Scroll to the bottom whenever a new message or the typing indicator appears
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  function handleSend() {
    const text = inputText.trim();
    if (!text) return;
    setInputText("");
    sendMessage(text).catch(() => {});
  }

  function handleSuggestedQuestion(question) {
    sendMessage(question).catch(() => {});
  }

  function handleKeyDown(event) {
    // Submit on Enter; allow newline with Shift+Enter
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  }

  const isEmptySession = messages.length === 0 && !isLoading;

  return (
    <Box sx={{ display: "flex", flexDirection: "column", height: "100%" }}>

      {/* Message history */}
      <Box sx={{ flex: 1, overflowY: "auto", p: 2 }}>

        {isEmptySession && (
          <Box sx={{ textAlign: "center", mt: 6, px: 2 }}>
            <Typography variant="body1" color="text.secondary" gutterBottom>
              Ask a question about the Fannie Mae Selling or Servicing Guide.
            </Typography>
            <Typography variant="caption" color="text.disabled" display="block" mb={3}>
              Try one of these to get started:
            </Typography>
            <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1, justifyContent: "center" }}>
              {SUGGESTED_QUESTIONS.map((question) => (
                <Chip
                  key={question}
                  label={question}
                  variant="outlined"
                  clickable
                  onClick={() => handleSuggestedQuestion(question)}
                  sx={{
                    borderColor: "secondary.main",
                    color: "secondary.main",
                    fontSize: "0.75rem",
                    "&:hover": {
                      backgroundColor: "rgba(0, 114, 206, 0.08)",
                    },
                  }}
                />
              ))}
            </Box>
          </Box>
        )}

        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}

        {isLoading && <TypingIndicator />}

        {errorMessage && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {errorMessage}
          </Alert>
        )}

        <div ref={messagesEndRef} />
      </Box>

      {/* Input area */}
      <Box sx={{ p: 2, borderTop: "1px solid", borderColor: "divider" }}>
        <TextField
          fullWidth
          multiline
          maxRows={4}
          placeholder="Ask about loan eligibility, property requirements, servicing guidelines..."
          value={inputText}
          onChange={(event) => setInputText(event.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton
                  onClick={handleSend}
                  disabled={isLoading || !inputText.trim()}
                  color="primary"
                  aria-label="Send message"
                >
                  <SendIcon />
                </IconButton>
              </InputAdornment>
            ),
          }}
        />
      </Box>
    </Box>
  );
}

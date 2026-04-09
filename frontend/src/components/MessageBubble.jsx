import { Avatar, Box, Typography } from "@mui/material";
import SourceCitations from "@/components/SourceCitations";


/**
 * Small circular avatar shown next to assistant messages.
 * Displays the FM initials in Fannie Mae navy.
 */
function AssistantAvatar() {
  return (
    <Avatar
      sx={{
        width: 32,
        height: 32,
        backgroundColor: "primary.main",
        fontSize: "0.6rem",
        fontWeight: "bold",
        flexShrink: 0,
        alignSelf: "flex-start",
        mt: 0.5,
      }}
    >
      FM
    </Avatar>
  );
}


/**
 * Renders a single message in the chat — either from the user or the assistant.
 *
 * User messages: right-aligned, FM navy background.
 * Assistant messages: left-aligned with FM blue accent border, FM avatar, and source citations.
 *
 * Props:
 *   message — { id, role: "user" | "assistant", content: string, sources?: array }
 */
export default function MessageBubble({ message }) {
  const isUser = message.role === "user";

  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
        alignItems: "flex-start",
        gap: 1,
        mb: 2,
      }}
    >
      {!isUser && <AssistantAvatar />}

      <Box
        sx={{
          maxWidth: "75%",
          px: 2,
          py: 1.5,
          borderRadius: 2,
          ...(isUser
            ? {
                backgroundColor: "primary.main",
                color: "primary.contrastText",
              }
            : {
                backgroundColor: "background.paper",
                color: "text.primary",
                border: "1px solid",
                borderColor: "divider",
                borderLeftColor: "secondary.main",
                borderLeftWidth: "3px",
              }),
        }}
      >
        <Typography variant="body2" sx={{ whiteSpace: "pre-wrap" }}>
          {message.content}
        </Typography>

        {!isUser && message.sources && (
          <SourceCitations sources={message.sources} />
        )}
      </Box>
    </Box>
  );
}

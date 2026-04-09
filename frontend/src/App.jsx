import { Box, Container, Paper, Typography } from "@mui/material";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import ChatWindow from "@/components/ChatWindow";

// Fannie Mae brand colors
const FM_NAVY = "#003087";
const FM_BLUE = "#0072CE";
const FM_BACKGROUND = "#EEF3FA";

const theme = createTheme({
  palette: {
    primary: {
      main: FM_NAVY,
      contrastText: "#ffffff",
    },
    secondary: {
      main: FM_BLUE,
      contrastText: "#ffffff",
    },
    background: {
      default: FM_BACKGROUND,
      paper: "#ffffff",
    },
  },
  typography: {
    fontFamily: '"Inter", "Helvetica Neue", Arial, sans-serif',
  },
  shape: {
    borderRadius: 8,
  },
});


/**
 * Root component. Sets up the Fannie Mae branded MUI theme and renders the chat layout.
 */
export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box
        sx={{
          minHeight: "100vh",
          backgroundColor: "background.default",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          py: 4,
        }}
      >
        <Container maxWidth="md">
          <Paper
            elevation={4}
            sx={{
              borderRadius: 3,
              overflow: "hidden",
              height: "82vh",
              display: "flex",
              flexDirection: "column",
            }}
          >
            {/* Branded header */}
            <Box
              sx={{
                px: 3,
                py: 2.5,
                backgroundColor: FM_NAVY,
                display: "flex",
                alignItems: "center",
                gap: 2,
              }}
            >
              {/* Logo mark */}
              <Box
                sx={{
                  width: 40,
                  height: 40,
                  borderRadius: "50%",
                  backgroundColor: FM_BLUE,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  flexShrink: 0,
                }}
              >
                <Typography
                  variant="subtitle2"
                  fontWeight="bold"
                  sx={{ color: "#ffffff", letterSpacing: 0.5 }}
                >
                  FM
                </Typography>
              </Box>

              {/* Title block */}
              <Box>
                <Typography
                  variant="h6"
                  fontWeight="bold"
                  sx={{ color: "#ffffff", lineHeight: 1.2 }}
                >
                  Fannie Mae Guide Assistant
                </Typography>
                <Typography variant="caption" sx={{ color: "rgba(255,255,255,0.7)" }}>
                  Answers grounded in the Selling Guide and Servicing Guide
                </Typography>
              </Box>
            </Box>

            {/* Chat area */}
            <Box sx={{ flex: 1, overflow: "hidden" }}>
              <ChatWindow />
            </Box>
          </Paper>
        </Container>
      </Box>
    </ThemeProvider>
  );
}

import { Accordion, AccordionDetails, AccordionSummary, Box, Typography } from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import ArticleIcon from "@mui/icons-material/Article";


/**
 * Renders the list of source document chunks retrieved for a given answer.
 * Collapsed by default — the user expands to see where the answer came from.
 *
 * Props:
 *   sources — array of { source_file, page_number, excerpt }
 *   Note: page_number is already 1-based (adjusted in the backend).
 */
export default function SourceCitations({ sources }) {
  if (!sources || sources.length === 0) return null;

  return (
    <Accordion
      disableGutters
      elevation={0}
      sx={{
        mt: 1,
        backgroundColor: "transparent",
        border: "1px solid",
        borderColor: "divider",
        borderRadius: 1,
        "&:before": { display: "none" },
      }}
    >
      <AccordionSummary
        expandIcon={<ExpandMoreIcon sx={{ color: "secondary.main" }} />}
      >
        <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
          <ArticleIcon fontSize="small" sx={{ color: "secondary.main" }} />
          <Typography variant="caption" color="text.secondary">
            {sources.length} source{sources.length !== 1 ? "s" : ""} retrieved
          </Typography>
        </Box>
      </AccordionSummary>

      <AccordionDetails sx={{ pt: 0 }}>
        {sources.map((source, index) => (
          <Box
            key={`${source.source_file}-${source.page_number ?? index}`}
            sx={{
              mb: 1.5,
              p: 1.5,
              borderRadius: 1,
              backgroundColor: "action.hover",
              borderLeft: "2px solid",
              borderLeftColor: "secondary.main",
            }}
          >
            <Typography variant="caption" fontWeight="bold" display="block">
              {source.source_file}
              {source.page_number != null ? ` — Page ${source.page_number}` : ""}
            </Typography>
            <Typography
              variant="caption"
              color="text.secondary"
              display="block"
              sx={{ mt: 0.5 }}
            >
              {source.excerpt}
            </Typography>
          </Box>
        ))}
      </AccordionDetails>
    </Accordion>
  );
}

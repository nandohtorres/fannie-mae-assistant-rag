import { Box, Divider, Typography } from "@mui/material";

const FM_NAVY = "#003087";
const FM_BLUE = "#0072CE";

const FACTS = [
  {
    label: "Est. 1938",
    detail:
      "Created by FDR's New Deal to stabilize home financing during the Great Depression.",
  },
  {
    label: "$4+ Trillion",
    detail:
      "Fannie Mae guarantees over $4 trillion in mortgage-backed securities — one of the largest in the world.",
  },
  {
    label: "Not a Lender",
    detail:
      "Fannie Mae doesn't lend to homebuyers directly. It buys mortgages from lenders so they can make more loans.",
  },
  {
    label: "The Name",
    detail:
      '"Fannie Mae" is a phonetic spelling of FNMA — Federal National Mortgage Association.',
  },
  {
    label: "2008 Crisis",
    detail:
      "Placed under federal conservatorship in September 2008 to stabilize the housing market.",
  },
  {
    label: "The Guides",
    detail:
      "The Selling & Servicing Guides set the rules lenders must follow for loans Fannie Mae purchases.",
  },
  {
    label: "Washington, D.C.",
    detail:
      "Headquartered in D.C., Fannie Mae operates as a government-sponsored enterprise (GSE).",
  },
];

/**
 * Left sidebar showing Fannie Mae fun facts.
 * Hidden on small screens via display breakpoint.
 */
export default function FunFactsSidebar() {
  return (
    <Box
      sx={{
        display: { xs: "none", md: "flex" },
        flexDirection: "column",
        width: 260,
        flexShrink: 0,
        backgroundColor: FM_NAVY,
        borderRadius: 3,
        overflow: "hidden",
        color: "#fff",
      }}
    >
      {/* Header */}
      <Box sx={{ px: 2.5, pt: 3, pb: 2 }}>
        <Typography
          variant="overline"
          sx={{ color: FM_BLUE, fontWeight: 700, letterSpacing: 1.5, fontSize: "0.65rem" }}
        >
          Did You Know?
        </Typography>
        <Typography variant="h6" fontWeight="bold" sx={{ lineHeight: 1.3, mt: 0.5 }}>
          Fannie Mae Facts
        </Typography>
      </Box>

      <Divider sx={{ borderColor: "rgba(255,255,255,0.1)" }} />

      {/* Facts list */}
      <Box sx={{ flex: 1, overflowY: "auto", px: 2.5, py: 2, display: "flex", flexDirection: "column", gap: 2.5 }}>
        {FACTS.map((fact) => (
          <Box key={fact.label}>
            <Box
              sx={{
                display: "inline-block",
                backgroundColor: FM_BLUE,
                borderRadius: 1,
                px: 1,
                py: 0.25,
                mb: 0.75,
              }}
            >
              <Typography variant="caption" fontWeight="bold" sx={{ color: "#fff", fontSize: "0.7rem" }}>
                {fact.label}
              </Typography>
            </Box>
            <Typography variant="body2" sx={{ color: "rgba(255,255,255,0.75)", lineHeight: 1.5, fontSize: "0.8rem" }}>
              {fact.detail}
            </Typography>
          </Box>
        ))}
      </Box>

      {/* Footer */}
      <Divider sx={{ borderColor: "rgba(255,255,255,0.1)" }} />
      <Box sx={{ px: 2.5, py: 1.5 }}>
        <Typography variant="caption" sx={{ color: "rgba(255,255,255,0.4)", fontSize: "0.65rem" }}>
          Source: fanniemae.com
        </Typography>
      </Box>
    </Box>
  );
}

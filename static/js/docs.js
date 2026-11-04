import { createApiReference } from "https://cdn.jsdelivr.net/npm/@scalar/api-reference/esm.js";

createApiReference("#scalar-reference", {
  url: "/openapi.json",
  theme: "deepSpace",
  forceDarkModeState: "dark",
  hideDarkModeToggle: true,
  withDefaultFonts: false,
  showDeveloperTools: "never",
  showSidebar: true,
});

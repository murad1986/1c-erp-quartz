import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

const config: QuartzConfig = {
  configuration: {
    pageTitle: "1C:ERP в Q-Commerce",
    pageTitleSuffix: "",
    enableSPA: true,
    enablePopovers: true,
    analytics: null,
    locale: "ru-RU",
    baseUrl: "localhost:8080",
    ignorePatterns: [
      "_meta",
      "**/_meta",
      "**/lesson_writer_agent.md",
      "**/promise_registry.md",
      "**/case_registry.md",
      "**/visual_prompts.md",
      "**/fact_check*",
      ".obsidian",
      "*.canvas",
      "**/.DS_Store",
      "README.md",
    ],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "IBM Plex Sans",
        body: "IBM Plex Sans",
        code: "IBM Plex Mono",
      },
      colors: {
        lightMode: {
          light: "#F5F8FF",
          lightgray: "#DDE4F0",
          gray: "#8A9AB5",
          darkgray: "#1E2D45",
          dark: "#0A1628",
          secondary: "#0055BB",
          tertiary: "#0077DD",
          highlight: "rgba(0, 85, 187, 0.08)",
          textHighlight: "#BFD4FF",
        },
        darkMode: {
          light: "#0D1B2E",
          lightgray: "#1A2D45",
          gray: "#4A6080",
          darkgray: "#B8CDE8",
          dark: "#E8F0FA",
          secondary: "#4D9EFF",
          tertiary: "#74B3FF",
          highlight: "rgba(77, 158, 255, 0.12)",
          textHighlight: "#1A3055",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: { light: "github-light", dark: "github-dark" },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents({ maxDepth: 3, minEntries: 2, showByDefault: true }),
      Plugin.CrawlLinks({
        markdownLinkResolution: "shortest",
        prettyLinks: true,
        lazyLoad: true,
        externalLinkIcon: true,
      }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({ enableSiteMap: true, enableRSS: true, rssLimit: 20 }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
    ],
  },
}

export default config

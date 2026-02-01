// docs/docusaurus.config.js
module.exports = {
  title: "SkySlots Docs",
  tagline: "VATSIM event planner & slot manager",
  url: "https://docs.skyslots.com", // set to your domain
  baseUrl: "/",
  onBrokenLinks: "warn",
  onBrokenMarkdownLinks: "warn",
  favicon: "static/img/logo.png",
  organizationName: "your-org", // GitHub org/user
  projectName: "skyslots",
  themeConfig: {
    navbar: {
      title: "SkySlots",
      logo: {
        alt: "SkySlots Logo",
        src: "img/logo.png",
      },
      items: [
        { to: "/docs/intro", label: "Docs", position: "left" },
        {
          href: "https://github.com/your-org/skyslots",
          label: "GitHub",
          position: "right",
        },
      ],
    },
    footer: {
      style: "dark",
      links: [
        {
          title: "Docs",
          items: [{ label: "Introduction", to: "/docs/intro" }],
        },
        {
          title: "Community",
          items: [
            { label: "GitHub", href: "https://github.com/your-org/skyslots" },
          ],
        },
      ],
      copyright: `© ${new Date().getFullYear()} SkySlots`,
    },
  },
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: "warn",
    },
  },
  presets: [
    [
      "@docusaurus/preset-classic",
      {
        docs: {
          path: "docs",
          routeBasePath: "docs",
          sidebarPath: require.resolve("./sidebars.js"),
        },
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      },
    ],
  ],
};

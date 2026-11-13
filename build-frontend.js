const fs = require("node:fs/promises");
const path = require("node:path");

const root = __dirname;
const outputDirectory = path.join(root, "dist");
const backendUrl = process.env.RENDER_API_URL;

if (!backendUrl) {
  throw new Error("Set RENDER_API_URL to the deployed Django API origin before building.");
}

const parsedBackendUrl = new URL(backendUrl);
if (!["http:", "https:"].includes(parsedBackendUrl.protocol) || parsedBackendUrl.pathname !== "/" || parsedBackendUrl.search || parsedBackendUrl.hash) {
  throw new Error("RENDER_API_URL must be an HTTP(S) origin without a path, query, or fragment.");
}

async function build() {
  await fs.mkdir(outputDirectory, { recursive: true });

  let html = await fs.readFile(path.join(root, "templates", "index.html"), "utf8");
  html = html.replace(/\s*\{% csrf_token %\}\s*/, "\n");
  await fs.writeFile(path.join(outputDirectory, "index.html"), html);

  await fs.cp(path.join(root, "static"), path.join(outputDirectory, "static"), {
    recursive: true,
  });
  const clientConfig = `window.PORTFOLIO_API_BASE_URL = ${JSON.stringify(parsedBackendUrl.origin)};\n`;
  await fs.writeFile(path.join(outputDirectory, "static", "js", "config.js"), clientConfig);
}

build().catch((error) => {
  console.error("Could not build the Vercel frontend.", error);
  process.exitCode = 1;
});

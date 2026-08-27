import { readFile, stat } from "node:fs/promises";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const marketplacePath = path.join(
  root,
  ".github",
  "plugin",
  "marketplace.json"
);
const marketplace = JSON.parse(await readFile(marketplacePath, "utf8"));

if (!Array.isArray(marketplace.plugins)) {
  throw new Error("marketplace.json must contain a plugins array");
}

const names = new Set();
const sources = new Set();

for (const entry of marketplace.plugins) {
  if (typeof entry.name !== "string" || typeof entry.source !== "string") {
    throw new Error("each marketplace plugin requires name and source");
  }
  if (names.has(entry.name) || sources.has(entry.source)) {
    throw new Error(`duplicate marketplace plugin: ${entry.name}`);
  }
  names.add(entry.name);
  sources.add(entry.source);

  const source = entry.source.replace(/^\.\//u, "");
  const pluginDirectory = path.resolve(root, source);
  const relative = path.relative(path.join(root, "plugins"), pluginDirectory);
  if (
    relative === "" ||
    path.isAbsolute(relative) ||
    relative.startsWith(`..${path.sep}`) ||
    relative.includes(path.sep)
  ) {
    throw new Error(`${entry.name}: source must be plugins/<name>`);
  }

  const manifestPath = path.join(pluginDirectory, "plugin.json");
  if (!(await stat(manifestPath)).isFile()) {
    throw new Error(`${entry.name}: source must contain plugin.json`);
  }
  const manifest = JSON.parse(await readFile(manifestPath, "utf8"));
  if (manifest.name !== entry.name) {
    throw new Error(`${entry.name}: manifest name does not match marketplace`);
  }
  if (manifest.version !== entry.version) {
    throw new Error(`${entry.name}: manifest version does not match marketplace`);
  }
}

console.log(`Validated ${marketplace.plugins.length} marketplace entries.`);

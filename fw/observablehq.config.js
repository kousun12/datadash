// See https://observablehq.com/framework/config for documentation.

import { fileURLToPath } from 'url';
import path from "path";
import fs from "fs";

function getPaths() {
  const __filename = fileURLToPath(import.meta.url);
  const __dirname = path.dirname(__filename);

  const dir = path.join(__dirname, '../chart_defs/sessions');
  const ids = fs.readdirSync(dir, { withFileTypes: true })
    .filter(dirent => dirent.isDirectory())
    .map(dirent => dirent.name);

  const allPaths = [];
  for (const id of ids) {
    const subPath = path.join(dir, id, "plot.md");
    if (fs.existsSync(subPath)) {
      const registerPath = path.join("/d/", id);
      allPaths.push(registerPath);
    }
  }
  return allPaths;
}

export default {
  title: "fred",

  // The pages and sections in the sidebar. If you don’t specify this option,
  // all pages will be listed in alphabetical order. Listing pages explicitly
  // lets you organize them into sections and have unlisted pages.
  // pages: [
  //   {
  //     name: "Examples",
  //     pages: [
  //       {name: "Dashboard", path: "/example-dashboard"},
  //       {name: "Report", path: "/example-report"}
  //     ]
  //   }
  // ],

  // Content to add to the head of the page, e.g. for a favicon:
  head: '<link rel="icon" href="observable.png" type="image/png" sizes="32x32">',

  // The path to the source root.
  root: "src",
  dynamicPaths: getPaths(),

  // Some additional configuration options and their defaults:
  theme: ["cotton", "alt", "wide"], // try "light", "dark", "slate", etc.
  header: "", // what to show in the header (HTML)
  footer: "", // what to show in the footer (HTML)
  sidebar: false, // whether to show the sidebar
  toc: false, // whether to show the table of contents
  pager: false, // whether to show previous & next links in the footer
  // output: "dist", // path to the output root for build
  // search: true, // activate search
  // linkify: true, // convert URLs in Markdown to links
  // typographer: false, // smart quotes and other typographic improvements
  // cleanUrls: true, // drop .html from URLs
};

import { fileURLToPath } from 'url';
import path from "path";
import fs from "fs";
import {parseArgs} from "node:util";

const {
  values: {uuid}
} = parseArgs({
  options: {uuid: {type: "string"}},
});

function getMdText(uuid) {
  const __filename = fileURLToPath(import.meta.url);
  const __dirname = path.dirname(__filename);
  const fp = path.join(__dirname, '../../../../chart_defs/sessions', uuid, "plot.md");
  return fs.readFileSync(fp, 'utf8');
}

process.stdout.write(getMdText(uuid));
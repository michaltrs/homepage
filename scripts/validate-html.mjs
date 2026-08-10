import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { HtmlValidate, formatterFactory } from 'html-validate';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PROJECT_ROOT = path.resolve(__dirname, '..');
const DIST_DIR = path.join(PROJECT_ROOT, 'dist');

function getHtmlFiles(dir) {
  let results = [];
  if (!fs.existsSync(dir)) return results;
  for (const file of fs.readdirSync(dir)) {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    if (stat.isDirectory()) {
      results = results.concat(getHtmlFiles(filePath));
    } else if (file.endsWith('.html')) {
      results.push(filePath);
    }
  }
  return results;
}

if (!fs.existsSync(DIST_DIR)) {
  console.error('[validate-html] Error: dist/ directory does not exist. Run the build first.');
  process.exit(1);
}

// Only validate pages actually rendered by Astro (have a canonical link tag).
// Legacy nested static HTML in public/archive/ (Doxygen dumps etc.) is marked
// noindex by post-build.mjs and lacks a canonical tag — it's excluded here on
// purpose: it's machine-generated third-party documentation from 2007-2008,
// already deprioritized for SEO, and not worth chasing to modern HTML5 validity.
const allHtmlFiles = getHtmlFiles(DIST_DIR);
const targetFiles = allHtmlFiles.filter((file) => {
  const content = fs.readFileSync(file, 'utf8');
  return content.includes('rel="canonical"');
});

console.log(`[validate-html] Found ${allHtmlFiles.length} HTML files, validating ${targetFiles.length} live (canonical) pages.\n`);

const htmlvalidate = new HtmlValidate({
  extends: ['html-validate:standard'],
});

let totalErrors = 0;
let totalWarnings = 0;
let filesWithProblems = 0;
const formatter = formatterFactory('stylish');
const allResults = [];

for (const file of targetFiles) {
  const report = await htmlvalidate.validateFile(file);
  allResults.push(...report.results);
  if (!report.valid) {
    filesWithProblems++;
  }
  totalErrors += report.errorCount;
  totalWarnings += report.warningCount;
}

const problemResults = allResults.filter((r) => r.errorCount > 0 || r.warningCount > 0);
if (problemResults.length > 0) {
  console.log(formatter(problemResults));
}

console.log(`\n=== HTML VALIDATION SUMMARY ===`);
console.log(`Live pages checked: ${targetFiles.length} (of ${allHtmlFiles.length} total HTML files in dist/)`);
console.log(`Files with problems: ${filesWithProblems}`);
console.log(`Errors: ${totalErrors}, Warnings: ${totalWarnings}\n`);

if (totalErrors > 0) {
  console.error('[validate-html] FAILED: fix the errors above.');
  process.exit(1);
}

console.log('[validate-html] OK: all live pages are valid HTML.');

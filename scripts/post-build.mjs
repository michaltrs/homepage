import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Paths
const PROJECT_ROOT = path.resolve(__dirname, '..');
const DIST_DIR = path.join(PROJECT_ROOT, 'dist');

console.log(`[post-build] Project root: ${PROJECT_ROOT}`);
console.log(`[post-build] Dist directory: ${DIST_DIR}\n`);

// Helper to get all HTML files recursively
function getHtmlFiles(dir) {
  let results = [];
  if (!fs.existsSync(dir)) return results;
  const list = fs.readdirSync(dir);
  list.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    if (stat && stat.isDirectory()) {
      results = results.concat(getHtmlFiles(filePath));
    } else if (file.endsWith('.html')) {
      results.push(filePath);
    }
  });
  return results;
}

if (!fs.existsSync(DIST_DIR)) {
  console.error(`[post-build] Error: dist/ directory does not exist. Run 'astro build' first.`);
  process.exit(1);
}

const htmlFiles = getHtmlFiles(DIST_DIR);
console.log(`[post-build] Found ${htmlFiles.length} HTML files to inspect.`);

let processedCount = 0;
let modifiedCount = 0;

for (const file of htmlFiles) {
  processedCount++;
  const relativePath = path.relative(DIST_DIR, file);
  const content = fs.readFileSync(file, 'utf8');

  // Check if the HTML file has a canonical tag
  // Standard Astro pages built with our Layout will have <link rel="canonical" ...>
  const hasCanonical = content.includes('rel="canonical"');

  if (!hasCanonical) {
    // This is a legacy raw HTML file lacking a user-selected canonical link.
    // Inject <meta name="robots" content="noindex, follow" /> to prevent Google indexing.
    const noindexTag = '\n    <meta name="robots" content="noindex, follow" />';
    
    let updatedContent = '';
    let successfullyInjected = false;

    // 1. Try case-insensitive <head> tag insertion
    const headMatch = content.match(/<head[^>]*>/i);
    if (headMatch) {
      const insertIndex = headMatch.index + headMatch[0].length;
      updatedContent = content.slice(0, insertIndex) + noindexTag + content.slice(insertIndex);
      successfullyInjected = true;
    } 
    // 2. Fallback to <html> tag if <head> is missing
    else {
      const htmlMatch = content.match(/<html[^>]*>/i);
      if (htmlMatch) {
        const insertIndex = htmlMatch.index + htmlMatch[0].length;
        updatedContent = content.slice(0, insertIndex) + noindexTag + content.slice(insertIndex);
        successfullyInjected = true;
      } 
      // 3. Last resort fallback: inject at the top of the file
      else {
        updatedContent = noindexTag + '\n' + content;
        successfullyInjected = true;
      }
    }

    if (successfullyInjected) {
      fs.writeFileSync(file, updatedContent, 'utf8');
      modifiedCount++;
      console.log(`[post-build] [NOINDEX INJECTED] dist/${relativePath}`);
    }
  }
}

console.log(`\n=== POST-BUILD SUMMARY ===`);
console.log(`Total HTML files processed: ${processedCount}`);
console.log(`Legacy files marked as noindex: ${modifiedCount}`);
console.log(`Astro pages kept unchanged: ${processedCount - modifiedCount}\n`);

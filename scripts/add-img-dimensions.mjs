import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import sizeOf from 'image-size';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Paths
const PROJECT_ROOT = path.resolve(__dirname, '..');
const ARCHIVE_DIR = path.join(PROJECT_ROOT, 'src/pages/archive');
const PUBLIC_DIR = path.join(PROJECT_ROOT, 'public');

console.log(`Project root: ${PROJECT_ROOT}`);
console.log(`Archive directory: ${ARCHIVE_DIR}`);
console.log(`Public directory: ${PUBLIC_DIR}\n`);

// Get all .astro files recursively
function getAstroFiles(dir) {
  let results = [];
  if (!fs.existsSync(dir)) return results;
  const list = fs.readdirSync(dir);
  list.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    if (stat && stat.isDirectory()) {
      results = results.concat(getAstroFiles(filePath));
    } else if (file.endsWith('.astro')) {
      results.push(filePath);
    }
  });
  return results;
}

// Regex to find <img> tags
// This matches <img ...> including self-closing and multiline tags
const IMG_TAG_REGEX = /<img\s+([^>]*?)>/gi;

function parseAttributes(tagContent) {
  const attrs = {};
  const attrRegex = /([a-zA-Z0-9_-]+)(?:\s*=\s*(?:(?:"([^"]*)")|(?:'([^']*)')|([^\s>]+)))?/gi;
  let match;
  while ((match = attrRegex.exec(tagContent)) !== null) {
    const name = match[1].toLowerCase();
    const value = match[2] !== undefined ? match[2] : (match[3] !== undefined ? match[3] : (match[4] || ""));
    attrs[name] = value;
  }
  return attrs;
}

const astroFiles = getAstroFiles(ARCHIVE_DIR);
console.log(`Found ${astroFiles.length} .astro files in the archive.\n`);

let totalImagesFound = 0;
let updatedImagesCount = 0;
let skippedImagesCount = 0;
let missingFilesCount = 0;

const isDryRun = process.argv.includes('--write') ? false : true;
if (isDryRun) {
  console.log("=== RUNNING IN DRY-RUN MODE (No files will be modified) ===");
  console.log("Run with '--write' flag to apply changes.\n");
} else {
  console.log("=== RUNNING IN WRITE MODE (Files will be modified in-place) ===\n");
}

for (const file of astroFiles) {
  const content = fs.readFileSync(file, 'utf8');
  let fileModified = false;

  // We'll replace matching img tags
  const modifiedContent = content.replace(IMG_TAG_REGEX, (fullTag, tagContent) => {
    totalImagesFound++;
    
    // Parse existing attributes
    const attrs = parseAttributes(tagContent);
    const src = attrs.src;

    if (!src) {
      console.log(`[WARNING] Image tag without src in ${path.relative(PROJECT_ROOT, file)}: ${fullTag}`);
      skippedImagesCount++;
      return fullTag;
    }

    // Skip external images
    if (src.startsWith('http://') || src.startsWith('https://') || src.startsWith('//')) {
      console.log(`[SKIP] External image: ${src}`);
      skippedImagesCount++;
      return fullTag;
    }

    // Skip if width and height already present
    if (attrs.width && attrs.height) {
      skippedImagesCount++;
      return fullTag;
    }

    // Resolve file path on disk
    let imgPathOnDisk = '';
    if (src.startsWith('/')) {
      imgPathOnDisk = path.join(PUBLIC_DIR, src);
    } else {
      // Map astro page file to its web URL directory in public/
      // e.g. src/pages/archive/cnk/vrcholy.astro -> archive/cnk/vrcholy/
      const relativeToPages = path.relative(path.join(PROJECT_ROOT, 'src/pages'), file);
      let urlPath = relativeToPages.replace(/\\/g, '/');
      if (urlPath.endsWith('.astro')) {
        urlPath = urlPath.slice(0, -6);
      }
      if (urlPath.endsWith('/index') || urlPath === 'index') {
        urlPath = urlPath.slice(0, -5);
      }
      
      const pageDirInPublic = path.join(PUBLIC_DIR, urlPath);
      imgPathOnDisk = path.join(pageDirInPublic, src);
    }

    if (!fs.existsSync(imgPathOnDisk)) {
      console.log(`[MISSING] Image file does not exist on disk: ${src} (checked ${imgPathOnDisk})`);
      missingFilesCount++;
      skippedImagesCount++;
      return fullTag;
    }

    try {
      // Read file into buffer to avoid compatibility issues with image-size package and Node path string reading
      const buffer = fs.readFileSync(imgPathOnDisk);
      const dimensions = sizeOf(buffer);
      const width = dimensions.width;
      const height = dimensions.height;

      if (!width || !height) {
        console.log(`[WARNING] Could not read dimensions for ${src}`);
        skippedImagesCount++;
        return fullTag;
      }

      // Add width and height to the tag
      let newTagContent = tagContent.trim();
      
      // Remove any trailing slashes to prevent issues
      const isSelfClosing = newTagContent.endsWith('/');
      if (isSelfClosing) {
        newTagContent = newTagContent.substring(0, newTagContent.length - 1).trim();
      }

      // Append width and height
      newTagContent += ` width="${width}" height="${height}"`;

      if (isSelfClosing) {
        newTagContent += ' /';
      }

      const replacement = `<img ${newTagContent}>`;
      console.log(`[UPDATE] ${path.relative(PROJECT_ROOT, file)}`);
      console.log(`   Old: ${fullTag}`);
      console.log(`   New: ${replacement} (${width}x${height})`);
      
      updatedImagesCount++;
      fileModified = true;
      return replacement;

    } catch (err) {
      console.log(`[ERROR] Failed to read image size for ${src}: ${err.message}`);
      skippedImagesCount++;
      return fullTag;
    }
  });

  if (fileModified && !isDryRun) {
    fs.writeFileSync(file, modifiedContent, 'utf8');
  }
}

console.log(`\n=== SUMMARY ===`);
console.log(`Total images found: ${totalImagesFound}`);
console.log(`Successfully updated: ${updatedImagesCount}`);
console.log(`Skipped (already have dimensions, or external): ${skippedImagesCount}`);
console.log(`Missing files on disk: ${missingFilesCount}`);
if (isDryRun && updatedImagesCount > 0) {
  console.log(`\nDry run finished. Run "node scripts/add-img-dimensions.mjs --write" to update files.`);
}

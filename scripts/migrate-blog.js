const fs = require('fs');
const path = require('path');
const { XMLParser } = require('fast-xml-parser');

const bloggerXmlPath = '/Users/misak/Workspace/homepage/michaltrs-hp-astro/scripts/blogger_feed.xml';
const outputDir = '/Users/misak/Workspace/homepage/michaltrs-hp-astro/src/content/vault';

if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

const xmlContent = fs.readFileSync(bloggerXmlPath, 'utf-8');
const parser = new XMLParser({
    ignoreAttributes: false,
    attributeNamePrefix: "@_"
});
const jsonObj = parser.parse(xmlContent);

// Atom feed uses 'entry' instead of 'item'
const entries = jsonObj.feed.entry;

// Milestones for blog posts
const blogMilestones = [
    "Svatba",
    "Moje první fotokniha",
    "Week of Life"
];

let migratedCount = 0;

entries.forEach(entry => {
    const title = entry.title['#text'] || entry.title || 'Untitled';
    const published = entry.published;
    const updated = entry.updated;
    const contentHtml = entry.content['#text'] || entry.content || '';

    // Find the alternate link (the viewable URL)
    const alternateLink = Array.isArray(entry.link)
        ? entry.link.find(l => l['@_rel'] === 'alternate')?.['@_href']
        : (entry.link?.['@_rel'] === 'alternate' ? entry.link?.['@_href'] : '');

    const isMilestone = blogMilestones.some(m => title.includes(m));
    const pubDate = new Date(published);

    // Create safe filename
    const dateStr = pubDate.toISOString().split('T')[0];
    const safeTitle = String(title).toLowerCase().replace(/ /g, '-').replace(/[^\w-]/g, '').substring(0, 30);
    const filename = `${dateStr}-${safeTitle}-blog.md`;

    const mdContent = `---
title: "${title.replace(/"/g, '\\"')}"
pubDate: ${pubDate.toISOString()}
updated: ${new Date(updated).toISOString()}
link: "${alternateLink}"
category: "blog"
isMilestone: ${isMilestone}
---

${contentHtml}
`;

    fs.writeFileSync(path.join(outputDir, filename), mdContent);
    migratedCount++;
});

console.log(`Blogger Migration Complete:`);
console.log(`- Migrated: ${migratedCount}`);

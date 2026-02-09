const fs = require('fs');
const path = require('path');
const { XMLParser } = require('fast-xml-parser');

const newsXmlPath = '/Users/misak/Workspace/homepage/www-2008-20/news.xml';
const outputDir = '/Users/misak/Workspace/homepage/michaltrs-hp-astro/src/content/vault';

if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

const xmlContent = fs.readFileSync(newsXmlPath, 'utf-8');
const parser = new XMLParser();
const jsonObj = parser.parse(xmlContent);

const items = jsonObj.rss.channel.item;

// Define milestones based on specific titles or strings
const milestones = [
    "Začátky práce na nové verzi stránek",
    "Moje promovaná Zuzinženýrka",
    "CVUT FEL"
];

// Content to skip
const skipKeywords = [
    "opravil jsem chybu",
    "v foto galerii",
    "v rámci mezí"
];

let migratedCount = 0;
let skippedCount = 0;

items.forEach(item => {
    const title = item.title;
    const pubDate = new Date(item.pubDate);
    const description = item.description || '';
    const link = item.link || '';

    // Check if we should skip
    const shouldSkip = skipKeywords.some(keyword => title.toLowerCase().includes(keyword.toLowerCase()));
    if (shouldSkip) {
        skippedCount++;
        return;
    }

    const isMilestone = milestones.some(m => title.includes(m));

    // Create safe filename
    const dateStr = pubDate.toISOString().split('T')[0];
    const safeTitle = title.toLowerCase().replace(/ /g, '-').replace(/[^\w-]/g, '').substring(0, 30);
    const filename = `${dateStr}-${safeTitle}.md`;

    const content = `---
title: "${title.replace(/"/g, '\\"')}"
pubDate: ${pubDate.toISOString()}
description: "${description.replace(/"/g, '\\"').replace(/\n/g, ' ')}"
link: "${link}"
category: "news"
isMilestone: ${isMilestone}
---

${description}
`;

    fs.writeFileSync(path.join(outputDir, filename), content);
    migratedCount++;
});

console.log(`Migration Complete:`);
console.log(`- Migrated: ${migratedCount}`);
console.log(`- Skipped: ${skippedCount}`);

const fs = require('fs');
const path = require('path');

const dir = path.join(__dirname, 'Round-1');
const teamName = 'Sujith Kumar AI ';

// The regex matches various forms of the placeholder
// We use a case-insensitive regex for the variations
const placeholderRegex = /\[Team Name Placeholder\]|Team Name Placeholder|TEAM_NAME|\<TEAM_NAME\>|TBD Team Name/gi;

let filesModified = 0;
let replacementsMade = 0;
const modifiedFilesList = [];

function walkAndReplace(currentPath) {
    const files = fs.readdirSync(currentPath);
    for (const file of files) {
        const fullPath = path.join(currentPath, file);
        if (fs.statSync(fullPath).isDirectory()) {
            walkAndReplace(fullPath);
        } else if (fullPath.endsWith('.md')) {
            let content = fs.readFileSync(fullPath, 'utf-8');
            let matchCount = (content.match(placeholderRegex) || []).length;
            
            if (matchCount > 0) {
                const newContent = content.replace(placeholderRegex, teamName);
                fs.writeFileSync(fullPath, newContent);
                filesModified++;
                replacementsMade += matchCount;
                modifiedFilesList.push(fullPath);
            }
        }
    }
}

walkAndReplace(dir);

console.log(JSON.stringify({
    filesModified,
    replacementsMade,
    modifiedFilesList
}));

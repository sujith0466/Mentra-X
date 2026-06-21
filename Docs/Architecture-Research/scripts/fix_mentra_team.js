const fs = require('fs');
const path = require('path');

const dir = path.join(__dirname, 'Round-1');
const searchString = 'Built by the Mentra Team | HiDevs × Mastra Hackathon 2026';
const replaceString = 'Built by Sujith Kumar AI | HiDevs × Mastra Hackathon 2026';

let count = 0;

function replaceInDir(currentDir) {
    const files = fs.readdirSync(currentDir);
    for (const file of files) {
        const fullPath = path.join(currentDir, file);
        if (fs.statSync(fullPath).isDirectory()) {
            replaceInDir(fullPath);
        } else if (fullPath.endsWith('.md')) {
            let content = fs.readFileSync(fullPath, 'utf8');
            if (content.includes(searchString)) {
                content = content.replace(new RegExp(searchString.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), replaceString);
                fs.writeFileSync(fullPath, content);
                console.log(`Updated: ${file}`);
                count++;
            }
        }
    }
}

replaceInDir(dir);
console.log(`Replaced in ${count} files.`);

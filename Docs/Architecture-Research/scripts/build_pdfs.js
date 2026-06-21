const fs = require('fs');
const path = require('path');

const dir = path.join(__dirname, 'Round-1');

function getFileContent(filename) {
    const filePath = path.join(dir, filename);
    if (fs.existsSync(filePath)) {
        return fs.readFileSync(filePath, 'utf-8');
    }
    console.warn(`Missing file: ${filename}`);
    return `[Missing Content: ${filename}]`;
}

function generatePRD() {
    const content = `---
title: Mentra X - Product Requirements Document
---

<div style="text-align: center; margin-top: 200px;">
  <h1>MENTRA X</h1>
  <h2>Product Requirements Document (PRD)</h2>
  <h3>AI-Powered Student Digital Twin</h3>
  <br/>
  <h4>Built By:<br/>Sujith Kumar AI</h4>
  <br/>
  <p>Track: Student Doubt-Solving & Learning Agent</p>
  <p>HiDevs × Mastra Hackathon 2026</p>
</div>

<div style="page-break-after: always;"></div>

## Table of Contents
1. Executive Summary
2. Problem Statement
3. Solution Summary
4. Target Users
5. User Journey
6. Student Digital Twin
7. Learning DNA
8. Features & Success Metrics
9. Future Vision

<div style="page-break-after: always;"></div>

# 1. Executive Summary
${getFileContent('Executive_Summary.md')}

<div style="page-break-after: always;"></div>

# 2. Solution Summary
${getFileContent('Solution_Summary.md')}

<div style="page-break-after: always;"></div>

# 3. Product Requirements
${getFileContent('PRD.md')}

---
Built by Sujith Kumar AI
HiDevs × Mastra Hackathon 2026
---
`;
    fs.writeFileSync(path.join(dir, 'PRD_final.md'), content);
}

function generateTechArch() {
    const content = `---
title: Mentra X - Technical Architecture
---

<div style="text-align: center; margin-top: 200px;">
  <h1>MENTRA X</h1>
  <h2>Technical Architecture Specification</h2>
  <h3>System Design, Mastra Swarm, and Safety Middleware</h3>
  <br/>
  <h4>Built By:<br/>Sujith Kumar AI</h4>
</div>

<div style="page-break-after: always;"></div>

## Table of Contents
1. Architecture Overview
2. Mastra Cognitive Swarm
3. Qdrant Memory Architecture
4. Enkrypt Safety Architecture
5. Digital Twin Design
6. Agent Workflows

<div style="page-break-after: always;"></div>

# 1. Architecture Overview
${getFileContent('Architecture_Overview.md')}

<div style="page-break-after: always;"></div>

# 2. Mastra Cognitive Swarm
${getFileContent('Mastra_Architecture.md')}

<div style="page-break-after: always;"></div>

# 3. Qdrant Memory Architecture
${getFileContent('Qdrant_Memory_Architecture.md')}

<div style="page-break-after: always;"></div>

# 4. Enkrypt Safety Architecture
${getFileContent('Enkrypt_Safety_Architecture.md')}

<div style="page-break-after: always;"></div>

# 5. Digital Twin Design
${getFileContent('Digital_Twin_Design.md')}

<div style="page-break-after: always;"></div>

# 6. Agent Workflows
${getFileContent('Agent_Workflows.md')}

---
Built by Sujith Kumar AI
HiDevs × Mastra Hackathon 2026
---
`;
    fs.writeFileSync(path.join(dir, 'Technical_Architecture_final.md'), content);
}

function generateSupporting() {
    const content = `---
title: Mentra X - Supporting Documents
---

<div style="text-align: center; margin-top: 200px;">
  <h1>MENTRA X</h1>
  <h2>Supporting Documentation & Evaluation</h2>
  <h3>Hackathon Readiness & Submission Assets</h3>
  <br/>
  <h4>Built By:<br/>Sujith Kumar AI</h4>
</div>

<div style="page-break-after: always;"></div>

## Table of Contents
1. Sample Student Session
2. Judge Scoring Report
3. Round-1 Final Readiness Report
4. Final Submission Package Manifest

<div style="page-break-after: always;"></div>

# 1. Sample Student Session
${getFileContent('Sample_Student_Session.md')}

<div style="page-break-after: always;"></div>

# 2. Judge Scoring Report
${getFileContent('Judge_Scoring_Report.md')}

<div style="page-break-after: always;"></div>

# 3. Round-1 Final Readiness Report
${getFileContent('Round1_Final_Readiness_Report.md')}

<div style="page-break-after: always;"></div>

# 4. Final Submission Package
${getFileContent('FINAL_SUBMISSION_PACKAGE.md')}

---
Built by Sujith Kumar AI
HiDevs × Mastra Hackathon 2026
---
`;
    fs.writeFileSync(path.join(dir, 'Supporting_Document_final.md'), content);
}

generatePRD();
generateTechArch();
generateSupporting();
console.log('Markdown consolidation complete.');

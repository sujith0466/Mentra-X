const fs = require('fs');
const path = require('path');

const dirs = [
  'src/pages/admin'
];

const replacements = [
  [/AI Swarm Architectures/gi, "AI Architectures"],
  [/AI Swarms/gi, "AI Tutors"],
  [/AI Swarm/gi, "AI Tutor"],
  [/agent swarm/gi, "AI team"],
  [/multi-agent swarms/gi, "AI tutors"],
  [/multi-agent swarm/gi, "AI tutor system"],
  [/multi-agent/gi, "advanced AI"],
  [/swarms/gi, "tutors"],
  [/swarm/gi, "tutor"],
  [/Mastra/gi, "Mentra"],
  [/Vector Memory Systems & Similarity Engineering/gi, "Natural Language Processing"],
  [/Vector Memory Systems & Embeddings Engineering/gi, "Natural Language Processing"],
  [/Vector Memory Engineering/gi, "Database Engineering"],
  [/Vector Embeddings/gi, "Study Profile"],
  [/Vector Memory/gi, "Learning Memory"],
  [/Vector Databases/gi, "Database Systems"],
  [/Vector DBs/gi, "Databases"],
  [/vector database/gi, "database"],
  [/vector embedding/gi, "learning data"],
  [/Qdrant/gi, "Database"],
  [/HNSW/gi, "Advanced"],
  [/cosine similarity/gi, "accuracy"],
  [/Digital Twin vector embeddings/gi, "learning profile data"],
  [/Digital Twin DNA/gi, "learning profile"],
  [/Cognitive Digital Twins/gi, "Personalized Learning Profiles"],
  [/Cognitive Digital Twin/gi, "Personalized Learning Profile"],
  [/Digital Twin tracking/gi, "progress tracking"],
  [/Digital Twin mutation/gi, "profile updates"],
  [/Digital Twins/gi, "Learning Profiles"],
  [/Digital Twin/gi, "Learning Profile"],
  [/cognitive twin/gi, "learning profile"],
  [/Enkrypt Layer 6 Safety Audited/gi, "Verified by AI Safety Monitors"],
  [/Enkrypt Security Layer 6 Protocols/gi, "AI Safety Protocols"],
  [/Enkrypt Security Layer/gi, "AI Safety System"],
  [/Enkrypt/gi, "Safety System"],
  [/SAFETY_VERIFIED/gi, "VERIFIED"],
  [/PII redaction heuristics/gi, "privacy protection rules"],
  [/PII redaction/gi, "privacy protection"],
  [/hallucination detection/gi, "fact checking"],
  [/Milestone Velocity/gi, "Completion Velocity"],
  [/Milestone Progress Roadmap/gi, "Progress Roadmap"]
];

function processDir(dir) {
  const fullPath = path.join(__dirname, dir);
  if (!fs.existsSync(fullPath)) return;
  
  const files = fs.readdirSync(fullPath);
  for (const file of files) {
    const filePath = path.join(fullPath, file);
    if (fs.statSync(filePath).isDirectory()) {
      processDir(path.join(dir, file));
    } else if (filePath.endsWith('.tsx') && !filePath.includes('DocumentationPage')) {
      let content = fs.readFileSync(filePath, 'utf8');
      let newContent = content;
      for (const [regex, replacement] of replacements) {
        newContent = newContent.replace(regex, replacement);
      }
      if (content !== newContent) {
        fs.writeFileSync(filePath, newContent, 'utf8');
        console.log('Updated ' + filePath);
      }
    }
  }
}

dirs.forEach(processDir);

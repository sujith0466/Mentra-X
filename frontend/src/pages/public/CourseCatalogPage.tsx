import React, { useState } from "react";
import { Link } from "react-router-dom";
import { Search, BookOpen, Clock, Award, CheckCircle2 } from "lucide-react";
import { Input } from "@/components/ui/Input";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";

export const CourseCatalogPage: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [activeCategory, setActiveCategory] = useState("All");

  const categories = ["All", "AI & Machine Learning", "Cloud & Systems", "Software Engineering", "Security & Governance"];

  const courses = [
    { id: "ai-101", title: "Advanced Agentic Coding & Orchestration", category: "AI & Machine Learning", desc: "Master Mastra swarms, multi-agent workflows, and tool execution.", level: "Advanced", modules: 12, duration: "24 hours", rating: "4.9 (180 reviews)" },
    { id: "cs-202", title: "Enterprise Cloud Architecture & Distributed Systems", category: "Cloud & Systems", desc: "Design fault-tolerant, high-concurrency microservices on AWS/GCP.", level: "Intermediate", modules: 8, duration: "16 hours", rating: "4.8 (142 reviews)" },
    { id: "ml-303", title: "Vector Memory Systems & Qdrant Engineering", category: "AI & Machine Learning", desc: "Build semantic search engines, hybrid search, and RAG pipelines.", level: "Advanced", modules: 10, duration: "20 hours", rating: "4.95 (210 reviews)" },
    { id: "sec-404", title: "AI Safety & Enkrypt Governance Layer Implementation", category: "Security & Governance", desc: "Implement output interceptors, PII redaction, and compliance auditing.", level: "Advanced", modules: 6, duration: "12 hours", rating: "5.0 (95 reviews)" },
    { id: "se-505", title: "Modern Enterprise Frontend Architecture with React 18", category: "Software Engineering", desc: "Build production SPA architectures with TanStack Query and Zustand.", level: "Intermediate", modules: 14, duration: "28 hours", rating: "4.85 (310 reviews)" },
  ];

  const filtered = courses.filter((c) => {
    const matchesCat = activeCategory === "All" || c.category === activeCategory;
    const matchesSearch = c.title.toLowerCase().includes(searchTerm.toLowerCase()) || c.desc.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesCat && matchesSearch;
  });

  return (
    <div className="space-y-8 py-6">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-obsidian-600 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold text-white">Enterprise Course Catalog</h1>
          <p className="text-sm text-slate-400 mt-1">Explore curriculum engineered for AI-era technology leadership.</p>
        </div>
        <div className="w-full md:w-80">
          <Input
            placeholder="Search courses by keyword..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            leftIcon={<Search className="w-4 h-4" />}
          />
        </div>
      </div>

      {/* Category Tabs */}
      <div className="flex flex-wrap gap-2">
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setActiveCategory(cat)}
            className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
              activeCategory === cat
                ? "bg-primary-600 text-white shadow-md shadow-indigo-500/20 border border-indigo-400/30"
                : "bg-obsidian-800 text-slate-400 hover:text-white hover:bg-obsidian-700 border border-obsidian-600"
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Course Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filtered.length > 0 ? (
          filtered.map((course) => (
            <Card key={course.id} variant="interactive" className="flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <Badge variant="purple" size="sm">{course.category}</Badge>
                  <Badge variant={course.level === "Advanced" ? "danger" : "primary"} size="sm">{course.level}</Badge>
                </div>
                <h3 className="text-lg font-bold text-white leading-snug">{course.title}</h3>
                <p className="text-xs text-slate-400 mt-2 leading-relaxed">{course.desc}</p>
                
                <div className="flex items-center space-x-4 mt-4 text-xs text-slate-500">
                  <span className="flex items-center gap-1"><BookOpen className="w-3.5 h-3.5" /> {course.modules} Modules</span>
                  <span className="flex items-center gap-1"><Clock className="w-3.5 h-3.5" /> {course.duration}</span>
                  <span className="flex items-center gap-1 text-amber-400"><Award className="w-3.5 h-3.5" /> {course.rating}</span>
                </div>
              </div>

              <div className="pt-4 mt-4 border-t border-obsidian-600 flex items-center justify-between">
                <span className="text-xs font-semibold text-emerald-400 flex items-center gap-1">
                  <CheckCircle2 className="w-3.5 h-3.5" /> Enkrypt Validated
                </span>
                <Link to={`/course/${course.id}`}>
                  <Button size="sm" variant="primary">View Syllabus</Button>
                </Link>
              </div>
            </Card>
          ))
        ) : (
          <div className="col-span-full py-12 text-center text-slate-500 text-sm">
            No courses found matching your search criteria.
          </div>
        )}
      </div>
    </div>
  );
};

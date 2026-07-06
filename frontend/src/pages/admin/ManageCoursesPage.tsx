import React from "react";
import { BookOpen, Plus, CheckCircle2 } from "lucide-react";
import { DataTable, Column } from "@/components/ui/DataTable";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";

export interface CourseRow {
  id: string;
  title: string;
  category: string;
  modules: number;
  students: number;
  aiTutor: "Enabled" | "Disabled";
  status: "Published" | "Draft";
}

export const ManageCoursesPage: React.FC = () => {
  const courses: CourseRow[] = [
    { id: "ai-101", title: "Advanced Agentic Coding & Orchestration", category: "AI & Machine Learning", modules: 12, students: 420, aiTutor: "Enabled", status: "Published" },
    { id: "cs-202", title: "Enterprise Cloud Architecture & Distributed Systems", category: "Cloud & Systems", modules: 8, students: 310, aiTutor: "Enabled", status: "Published" },
    { id: "ml-303", title: "Vector Memory Systems & Embeddings Engineering", category: "AI & Machine Learning", modules: 10, students: 280, aiTutor: "Enabled", status: "Published" },
    { id: "sec-404", title: "AI Safety & Governance Layer Implementation", category: "Security & Governance", modules: 6, students: 150, aiTutor: "Enabled", status: "Published" },
  ];

  const columns: Column<CourseRow>[] = [
    { key: "id", title: "Course Code", sortable: true, render: (item) => <span className="font-mono text-xs text-indigo-400">{item.id}</span> },
    { key: "title", title: "Course Title", sortable: true, render: (item) => <span className="font-bold text-white">{item.title}</span> },
    { key: "category", title: "Domain", sortable: true, render: (item) => <Badge variant="purple" size="sm">{item.category}</Badge> },
    { key: "modules", title: "Syllabus", sortable: true, render: (item) => <span className="text-slate-300">{item.modules} Modules</span> },
    { key: "students", title: "Enrollments", sortable: true, render: (item) => <span className="font-mono text-emerald-400 font-bold">{item.students} Students</span> },
    { key: "aiTutor", title: "AI Swarm", render: (item) => <Badge variant="cyan" size="sm">{item.aiTutor}</Badge> },
    { key: "status", title: "Status", render: (item) => <Badge variant="success" size="sm">{item.status}</Badge> },
    { key: "actions", title: "Actions", render: () => <Button size="sm" variant="outline">Edit Syllabus</Button> }
  ];

  return (
    <div className="space-y-8 py-6">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-obsidian-600 pb-6">
        <div>
          <Badge variant="danger" size="sm">Admin Management</Badge>
          <h1 className="text-3xl font-extrabold text-white mt-1">Syllabus & Course Catalog Management</h1>
          <p className="text-sm text-slate-400 mt-1">Configure AI tutor embeddings, syllabus prerequisites, and vector indexing.</p>
        </div>
        <Button size="md" leftIcon={<Plus className="w-4 h-4" />}>
          Create New Enterprise Course
        </Button>
      </div>

      <Card variant="default" className="p-6">
        <DataTable
          data={courses}
          columns={columns}
          searchKey="title"
          searchPlaceholder="Search courses by title..."
        />
      </Card>
    </div>
  );
};
